# PID Tuning



| Type | Kp  | Ki  | Kd  |
| ---- | --- | --- | --- |
| PI   | 20  | 10  | 0   |

![](https://i.imgur.com/unygf4p.png)

Minimum velocity: -1.87 units/s
Time taken to attain cruise control: 20s

For Kp=nbd(20) & Ki=nbd(10), the controller acts as a PI regulator and operates at the cruise control set velocity.
Further investigation has to be done to understand the reason behind this.
With 0<Kd<10 the PID version works similar to PI.

But with this setup, initially the car goes backwards with nearly 2 units/s velocity which is undesirable.

Only proportional gain is able to fix the initial negative velocity.


---



| Type    | Kp | Ki    |Kd |
| -------- | -------- | --- | --|
| PID | 25     |  10   | 25     |

![](https://i.imgur.com/eIBtWHC.png)

Min velocity: -1.24 units/s
Time taken to attain cruise control: 23s

Increasing proportional gain decreases the backward motion of the car in the beginning. But rise in integral gain is causing the car to exceed the reference 70 units/s speed.



---



| Type    | Kp | Ki | Kd |
| --- | -------- | -------- | -------- |
|    PID| 45   | 15     | 20    |

![](https://i.imgur.com/LKaQtmv.png)

* Doesn't move back in the beginning
* Time taken to attain cruise control: 13s
* Quick acceleration
* But reaches 72 units/s---undesirable


---

| Type | Kp  | Ki  | Kd  |
| ---- | --- | --- | --- |
| PID   | 120  | 20  | 50   |

![](https://i.imgur.com/rKkWk1W.png)

* Fastest Gain
* Time taken:13s
* Maintains near ideal cruise control
* Doesn't go backward in the beginning
* But too fast of an acceleration which might not be safe for on-road vehicles

The derivative gain is very sensitive and operates in the optimal manner in a small window.
At Kd=43, time taken was t=15s
![](https://i.imgur.com/mzflY0w.png)

At Kd=56, the time taken is 12 seconds.
![](https://i.imgur.com/MHp1y9U.png)


But beyond this there are fluctuations and erratic gain and drop at certain values and intervals.



---

| Type | Kp  | Ki  | Kd  |
| ---- | --- | --- | --- |
| PID   | 70  | 16  | 40   |

![](https://i.imgur.com/IKcrs0K.png)

* Good acceleration without much jumps in speeds in an instant
* Attains cruise control in 14 seconds
* An optimum setup for the car

Ki less than 16 is not enough to reach the reference speed while Ki>17 causes overshoot making the range for integral gain quite small.
This is generally the case in different scenarios that the integral gain is quite sensitive to underhoot or overshoot and working in desired way in a small range.

---

| Type | Kp  | Ki  | Kd  |
| ---- | --- | --- | --- |
| PID   | 80  | 16.5  | 40   |

![](https://i.imgur.com/IJeBm3U.png)

With a significant increase in proportional gain, even a small increase in integral gain without increase in differential gain is sufficient to attain steady-state.

---

| Type | Kp  | Ki  | Kd  |
| ---- | --- | --- | --- |
| PID   | 150  | 23  | 20   |

* Time taken= 10 seconds
* System is quite sensitive to derivative gain after a certain value making the system unstable
* Integral gain is needed to be relatively small for higher proprtional gain to avoid overshoot

---

| Type | Kp  | Ki  | Kd  |
| ---- | --- | --- | --- |
| PID   | 10  | 8  | 10   |

![](https://i.imgur.com/dNhDZym.png)

* Too slow of a gain
* Would move backward in beginning
* But a safe setup if above mentioned is removed

---
| Type | Kp  | Ki  | Kd  |
| ---- | --- | --- | --- |
| PID   | 100  | 19  | 40   |

![](https://i.imgur.com/KY6bF1p.png)

* Time taken = 12s
* Quick acceleration



---

| Type | Kp  | Ki  | Kd  |
| ---- | --- | --- | --- |
| PID   | 30  | 11  | 40   |

![](https://i.imgur.com/hDUnzD1.png)

* Safe and optimum acceleration
* Quick gain with time taken being around 18 seconds
* Minimum velocity=-0.4 units/s---minimized backward movement

All in all this is very good setup for cruise control as it assures safe running without compromising on acceleration. 

---

| Type | Kp  | Ki  | Kd  |
| ---- | --- | --- | --- |
| PI   | 20  | 10  | 0   |
| PID | 25     |  10   | 25     |
|    PID| 45   | 15     | 20    |
| PID   | 120  | 20  | 50   |
| PID   | 70  | 16  | 40   |
|PID   | 80  | 16.5  | 40   |
| PID   | 150  | 23  | 20   |
| PID   | 10  | 8  | 10   |
| PID   | 100  | 19  | 40   |
| PID   | 30  | 11  | 40   |




So from all this,it can be observed that proportional gain is responsible for quick gain in speed, integral gain can lead to overshoot if not not tuned properly and differential gain can help reach reference or decrease overshoot.

Different combinations can at times give the same output on a broad scale.