#define SIZE 5

uint8_t FORW_TRIG = A4;
uint8_t FORW_ECHO = A5;
uint8_t LEFT_TRIG = A1;
uint8_t LEFT_ECHO = A0;
uint8_t RIGHT_TRIG = A3;
uint8_t RIGHT_ECHO = A2;

#define PPR 512   // Pulses per rotation
#define DIAM_MM 34    // Wheel diameter in mm
#define PI 3.14159265359
#define CELL_LENGTH 158   // Maze cell dimension in mm
#define WHL_DIST 81   // Distance between wheels (Turning diameter) in mm

#define SPEED 200

#define KP 40
#define KD 200
#define TARGET 4.8

float TURN_DIST = PI * WHL_DIST / 4;   // Distance wheel has to move for quarter turn (90 degrees) (Right or left)
float WHL_CIRCMF = DIAM_MM * PI;  // Distance moved by wheel in 1 rotation in mm
float PULSES_PER_MM = PPR / WHL_CIRCMF;   // Pulses in 1 mm rotation of wheel

float FORW_PULSES = CELL_LENGTH * PULSES_PER_MM;  // Pulses for moving 1 cell length
float TURN_PULSES = TURN_DIST * PULSES_PER_MM;  // Pulses for turning 90 degrees

#define ENC_L 2
#define PWM_L 10
#define IN1_L 6
#define IN2_L 7

#define ENC_R 3
#define PWM_R 11
#define IN1_R 8
#define IN2_R 9


typedef struct Pos
{
    int x;
    int y;
} Pos;


typedef struct Node
{
    Pos pos;
    struct Node *next;
} Node;


typedef struct Queue
{
    Node *head;
    Node *tail;
} Queue;


typedef struct Cell
{
    int N;
    int E;
    int S;
    int W;
    int val;
} Cell;


typedef struct Motor
{
    int encPin;
    int in1;
    int in2;
    int pwmPin;
    volatile int posi;
    int pwr;
    int dir;
} Motor;


typedef struct Sensor
{
    uint8_t trig;
    uint8_t echo;
} Sensor;


Motor motors[2] = {{ENC_L, IN1_L, IN2_L, PWM_L, 0, 0, 0}, {ENC_R, IN1_R, IN2_R, PWM_R, 0, 0, 0}};

Sensor sensors[2] = {{LEFT_TRIG, LEFT_ECHO}, {RIGHT_TRIG, RIGHT_ECHO}};

Cell maze_map[SIZE][SIZE];

float eprev[2] = {0, 0};


void Enqueue(Queue *queue, Pos curpos)
{
    Node *temp = (Node *)malloc(sizeof(Node));
    
    if (temp == NULL) return;

    (temp -> pos).x = curpos.x;
    (temp -> pos).y = curpos.y;
    temp -> next = NULL;

    if (queue -> tail != NULL) 
        queue -> tail -> next = temp;
    else 
        queue -> head = temp;

    queue -> tail = temp;
}


Pos Dequeue(Queue *queue)
{
    if (queue->head == NULL) return (Pos){-1, -1};

    Node *temp = queue -> head -> next;
    Pos curpos = queue -> head -> pos;

    free(queue -> head);
    queue -> head = temp;

    if (temp == NULL)
        queue -> tail = temp;

    return curpos;
}


void Flood(Cell maze_map[SIZE][SIZE], Pos goal)
{
    maze_map[goal.x][goal.y].val = 0;
    
    Queue queue = {NULL, NULL};
    Enqueue(&queue, goal);

    Pos curpos, pos;
    Pos pos_change[4] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

    int visited[SIZE][SIZE];

    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            visited[i][j] = 0;
        }
    }

    while (queue.head != NULL)
    {
        curpos = Dequeue(&queue);
        visited[curpos.x][curpos.y] = 1;

        int wall_info[4] = {maze_map[curpos.x][curpos.y].N, maze_map[curpos.x][curpos.y].S, maze_map[curpos.x][curpos.y].W, maze_map[curpos.x][curpos.y].E};

        for (int i = 0; i < 4; i++)
        {
            pos.x = curpos.x + pos_change[i].x;
            pos.y = curpos.y + pos_change[i].y;

            if (wall_info[i] == 1 && visited[pos.x][pos.y] == 0)
            {
                Enqueue(&queue, pos);
                maze_map[pos.x][pos.y].val = maze_map[curpos.x][curpos.y].val + 1;
            }
        }
    }
}


int NextPosFinder(Cell maze_map[SIZE][SIZE], Pos curpos)
{
    Pos pos_change[4] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    int wall_info[4] = {maze_map[curpos.x][curpos.y].N, maze_map[curpos.x][curpos.y].E, maze_map[curpos.x][curpos.y].S, maze_map[curpos.x][curpos.y].W};

    Pos pos;
    int leastval = maze_map[curpos.x][curpos.y].val;
    int bestdir;

    for (int i = 0; i < 4; i++)
    {
        pos.x = curpos.x + pos_change[i].x;
        pos.y = curpos.y + pos_change[i].y;

        if (wall_info[i] == 1 && maze_map[pos.x][pos.y].val < leastval)
        {
            leastval = maze_map[pos.x][pos.y].val;
            bestdir = i;
        }
    }
    
    return bestdir;
}


int DetectWall(uint8_t trig, uint8_t echo)
{
    float avg_dist = 0, echo_time, dist;
    int count = 0;

    for (int i = 0; i < 5; i++)
    {
        digitalWrite(trig, LOW);
        delayMicroseconds(1);
        digitalWrite(trig, HIGH);
        delayMicroseconds(10);
        digitalWrite(trig, LOW);

        echo_time = pulseIn(echo, HIGH);
        dist = echo_time * 0.017;

        Serial.print(dist);
        Serial.print("\t");

        if (dist < 100) 
        {
          avg_dist += dist;
          count++;
        }
        
        delay(50);
    }
    Serial.println();
    
    if (count == 0) return 1;

    avg_dist /= count;

    Serial.print("Avg Dist: ");
    Serial.println(avg_dist);

    if (avg_dist < 8.0) return 0;
    return 1;
}


void UpdateMap(Cell maze_map[SIZE][SIZE], Pos curpos, int orient_int)
{
    int wall_info[4] = {maze_map[curpos.x][curpos.y].N, maze_map[curpos.x][curpos.y].E, maze_map[curpos.x][curpos.y].S, maze_map[curpos.x][curpos.y].W};

    int sensor_info[3][2] = {{LEFT_TRIG, LEFT_ECHO}, {FORW_TRIG, FORW_ECHO}, {RIGHT_TRIG, RIGHT_ECHO}};
    char sensor[3][10] = {"Left: ", "Forw: ", "Right: "};
    int wall_index;

    if (orient_int == 0) wall_index = 3;
    else wall_index = orient_int - 1;

    for (int i = 0; i < 3; i++)
    {
        Serial.println(sensor[i]);

        wall_info[wall_index] = DetectWall(sensor_info[i][0], sensor_info[i][1]);

        wall_index += 1;
        if (wall_index > 3) wall_index = 0;

        delay(50);
    }

    Serial.print("N: ");
    Serial.println(wall_info[0]);
    Serial.print("E: ");
    Serial.println(wall_info[1]);
    Serial.print("S: ");
    Serial.println(wall_info[2]);
    Serial.print("W: ");
    Serial.println(wall_info[3]);

    maze_map[curpos.x][curpos.y].N = wall_info[0];
    if (curpos.x - 1 >= 0) maze_map[curpos.x - 1][curpos.y].S = wall_info[0];

    maze_map[curpos.x][curpos.y].E = wall_info[1];
    if (curpos.y + 1 < SIZE) maze_map[curpos.x][curpos.y + 1].W = wall_info[1];

    maze_map[curpos.x][curpos.y].S = wall_info[2];
    if (curpos.x + 1 < SIZE) maze_map[curpos.x + 1][curpos.y].N = wall_info[2];
    
    maze_map[curpos.x][curpos.y].W = wall_info[3];
    if (curpos.y - 1 >= 0) maze_map[curpos.x][curpos.y - 1].E = wall_info[3];
}


void InitializeMazeMap(Cell maze_map[SIZE][SIZE])
{
    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            maze_map[i][j].N = 1;
            maze_map[i][j].E = 1;
            maze_map[i][j].S = 1;
            maze_map[i][j].W = 1;
            maze_map[i][j].val = -1;

            if (i == 0) maze_map[i][j].N = 0;
            if (i == SIZE-1) maze_map[i][j].S = 0;
            if (j == 0) maze_map[i][j].W = 0;
            if (j == SIZE-1) maze_map[i][j].E = 0;
        }
    }
}


char DirFinder(int orient_int, int dir_int, Pos *curpos)
{
    char rel_dir_mapping[] = "FLBR";
    int dir_diff;

    if (dir_int == 0)
    {
        dir_diff = orient_int - 0;
        curpos -> x -= 1;
    }
    if (dir_int == 1)
    {
        dir_diff = orient_int - 1;
        curpos -> y += 1;
    }
    if (dir_int == 2)
    {
        dir_diff = orient_int - 2;
        curpos -> x += 1;
    }
    if (dir_int == 3)
    {
        dir_diff = orient_int - 3;
        curpos -> y -= 1;
    }

    if (dir_diff < 0) dir_diff = 4 + dir_diff;

    return rel_dir_mapping[dir_diff];
}


void setMotor(int motorIndex)
{
    analogWrite(motors[motorIndex].pwmPin, motors[motorIndex].pwr);

    if (motors[motorIndex].dir == 1)
    {
      digitalWrite(motors[motorIndex].in1, HIGH);
      digitalWrite(motors[motorIndex].in2, LOW);
    }

    else if (motors[motorIndex].dir == -1)
    {
      digitalWrite(motors[motorIndex].in1, LOW);
      digitalWrite(motors[motorIndex].in2, HIGH);
    }

    else
    {
      digitalWrite(motors[motorIndex].in1, LOW);
      digitalWrite(motors[motorIndex].in2, LOW);
    }  
}


void RunMotors(int targets[2])
{
    int target = (int) fabs(targets[0]);
    int avg;

    motors[0].pwr = SPEED;
    motors[0].dir = 1;
    motors[1].pwr = SPEED;
    motors[1].dir = 1;

    if (targets[0] < 0) motors[0].dir = -1;
    if (targets[1] < 0) motors[1].dir = -1;
    
    setMotor(0);
    setMotor(1);

    do
    {
      noInterrupts();
      avg = (motors[0].posi + motors[1].posi) / 2;
      interrupts();
      Serial.println(avg);
      delay(10);
    }
    while (avg < target);

    motors[0].pwr = 0;
    motors[0].dir = 0;
    motors[1].pwr = 0;
    motors[1].dir = 0;
    
    setMotor(0);
    setMotor(1);

    noInterrupts();
    motors[0].posi = 0;
    motors[1].posi = 0;
    interrupts();
}


void MoveMouse(char dir)
{
    int targets[2];

    if (dir == 'R')
    {
        targets[0] = TURN_PULSES;
        targets[1] = -TURN_PULSES;
        RunMotors(targets);
    }
    else if (dir == 'L')
    {
        targets[0] = -TURN_PULSES;
        targets[1] = TURN_PULSES;
        RunMotors(targets);
    }
    else if (dir == 'B')
    {
        targets[0] = 2 * TURN_PULSES;
        targets[1] = -2 * TURN_PULSES;
        RunMotors(targets);
    }
    Serial.println("Done1");
    delay(1000);

    // targets[0] = FORW_PULSES;
    // targets[1] = FORW_PULSES;
    // RunMotors(targets);

    ForwCorr(FORW_PULSES);

    Serial.println("Done2");
}


template <int i>
void encoderISR()
{   
    // motors[i].posi += motors[i].dir;
    motors[i].posi += 1;
}


float DistMeasure(int SensorIndex)
{
    float echo_time, dist;

    digitalWrite(sensors[SensorIndex].trig, LOW);
    delayMicroseconds(1);
    digitalWrite(sensors[SensorIndex].trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(sensors[SensorIndex].trig, LOW);

    echo_time = pulseIn(sensors[SensorIndex].echo, HIGH);
    dist = echo_time * 0.017;

    Serial.print(dist);
    Serial.print("\t");

    return dist;
} 


void SpeedCorrection(int SensorIndex)
{
    float dist = DistMeasure(SensorIndex);

    if (dist > 10) 
    {
      eprev[SensorIndex] = 0;
      return;
    }

    float err = TARGET - dist;

    if (fabs(err) < 0.3) err = 0;

    float graderr = 0;

    if (err > 0 && eprev[SensorIndex] > 0 || err < 0 && eprev[SensorIndex] < 0)
        graderr = err - eprev[SensorIndex];

    int correction = KP * err + (KD * graderr);

    if (correction > SPEED - 70) correction = SPEED - 70;
    if (correction < 70 - SPEED) correction = 70 - SPEED;

    Serial.print(err);
    Serial.print("\t");
    Serial.println(correction);
    
    if (correction > 0) 
    {
      motors[1 - SensorIndex].pwr = SPEED - correction;
      motors[SensorIndex].pwr = SPEED;
    }
    else 
    {
      motors[SensorIndex].pwr = SPEED + correction;
      motors[1 - SensorIndex].pwr = SPEED;
    }

    eprev[SensorIndex] = err;
}


void ForwCorr(int target)
{
    int avg;

    motors[0].pwr = SPEED;
    motors[0].dir = 1;
    motors[1].pwr = SPEED;
    motors[1].dir = 1;

    do
    {
      SpeedCorrection(0);
      SpeedCorrection(1);

      setMotor(0);
      setMotor(1);

      noInterrupts();
      avg = (motors[0].posi + motors[1].posi) / 2;
      interrupts();

      Serial.println(avg);

      delay(30);
    }
    while (avg < target);

    motors[0].pwr = 0;
    motors[0].dir = 0;
    motors[1].pwr = 0;
    motors[1].dir = 0;
    
    setMotor(0);
    setMotor(1);

    noInterrupts();
    motors[0].posi = 0;
    motors[1].posi = 0;
    interrupts();

    eprev[0] = 0;
    eprev[1] = 0;
}


void setup()
{
    Serial.begin(9600);

    pinMode(FORW_ECHO, INPUT);
    pinMode(FORW_TRIG, OUTPUT);
    pinMode(RIGHT_ECHO, INPUT);
    pinMode(RIGHT_TRIG, OUTPUT);
    pinMode(LEFT_ECHO, INPUT);
    pinMode(LEFT_TRIG, OUTPUT);

    for (int i = 0; i < 2; i++)
    {
        pinMode(motors[i].encPin, INPUT);
        pinMode(motors[i].pwmPin, OUTPUT);
        pinMode(motors[i].in1, OUTPUT);
        pinMode(motors[i].in2, OUTPUT);
    }

    attachInterrupt(digitalPinToInterrupt(motors[0].encPin), encoderISR<0>, RISING);
    attachInterrupt(digitalPinToInterrupt(motors[1].encPin), encoderISR<1>, RISING);
}

    
void loop() 
{   
    InitializeMazeMap(maze_map);

    Pos start = {SIZE - 1, SIZE - 1};
    Pos goal = {SIZE/2, SIZE/2};

    Pos curpos = {start.x, start.y};

    char dir, orient;
    int dir_int, orient_int = 0;

    char dir_mapping[5] = "NESW";

    delay(100);
    Serial.println();

    while (curpos.x != goal.x || curpos.y != goal.y)
    {   
        orient = dir_mapping[orient_int];

        Serial.print(curpos.x);
        Serial.print(", ");
        Serial.println(curpos.y);
        Serial.print("Orient: ");
        Serial.println(orient);
        
        UpdateMap(maze_map, curpos, orient_int);

        Flood(maze_map, goal);
        
        dir_int = NextPosFinder(maze_map, curpos);

        dir = DirFinder(orient_int, dir_int, &curpos);

        orient_int = dir_int;

        Serial.println(dir_mapping[dir_int]);
        Serial.println(dir);

        MoveMouse(dir);

        delay(1000);
    }
    
    Serial.println("You have reached the goal!");
    Serial.println("Resetting...");
    delay(5000);
}
