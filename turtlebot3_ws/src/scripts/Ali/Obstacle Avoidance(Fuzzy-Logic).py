import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile, ReliabilityPolicy



class Fuzzyobstacleavoidance:

    def __init__(self,RB_dist,RF_dist):
        self.RB_dist=RB_dist
        self.RF_dist=RF_dist

RB_dist=fuzzy_instance.RB_dist
RF_dist=fuzzy_instance.RF_dist



#----------------STEP1 MAPPING OF INPUT AND OUTPUT SPACE-------------------
class Membershipfunction:

    def __init__(self, Points, label):
        # Takes four point as input (Points) for the trapozial membership. The center triangle is special case of
        # trpozide where two points are same forming the triangle [0.25, 0.5, 0.5, 0.75], labels gives labels for
        # the member values ie far, medium, near

        self.points = Points
        self.linguistic_label = label

    def getMemberValue(self, input_value):  # to get membership value from input sensor value

        # if input value outside the trapozidal Range the return is zero
        if input_value < self.points[0] or input_value > self.points[3]:
            return 0.0

        # Rising edge formula implementation (x-a)/(b-a) since self.point is list extract value by index
        elif input_value >= self.points[0] and input_value < self.points[1]:
            return (input_value - self.points[0]) / (self.points[1] - self.points[0])

        # Falling edge formula implementation (c-x)/(c-b) since self.point is list extract value by index
        elif input_value > self.points[2] and input_value < self.points[3]:
            return (self.points[3] - input_value) / (self.points[3] - self.points[2])

        # if input value at the plateue of trapozid return 1
        elif input_value >= self.points[1] and input_value <= self.points[2]:
            return 1.0

        return 0.0


# assigning range to close, medium and fast


close_RB_Dist = Membershipfunction([0.1, 0.1, 0.3, 0.5], 'close')
close_RF_Dist = Membershipfunction([0.1, 0.1, 0.3, 0.5], 'close')

med_RB_Dist = Membershipfunction([0.3, 0.5, 0.5, 0.8], 'med')
med_RF_Dist = Membershipfunction([0.3, 0.5, 0.5, 0.8], 'med')

far_RB_Dist = Membershipfunction([0.8, 0.8, 1.0 , 1.0], 'far')
far_RF_Dist = Membershipfunction([0.8, 0.8, 1.0 , 1.0], 'far')

slow_Dist = Membershipfunction([0.0, 0.1], 'slow')
med_Dist = Membershipfunction([0.1, 0.3], 'med')
fast_Dist = Membershipfunction([0.3, 0.5], 'fast')


#Step 2------------Define the rule Base----------------


class rule:

    def __init__(self, i, o):
        # Makes the rule base. where i=inputs RFS and RBS ( and o=outputs (Turning and speed). The rule base is initiated
        # blow this block of code. Check blew this code blow to check input and outputs
        self.inputs = i
        self.outputs = o

    def getFir(self, list_Values):
        # to get firing strength: List value are  List of [RFS, RBS] where the list is has two elemnts each dictonary
        # if RB_dist = 0.3 and RF_dist = 0.6 as in lab example its prints out list with two dictionaries
        #list_Values= [{'close': 0.0, 'med': 0.6000000000000001, 'far': 0.3999999999999999},{'close': 0.8, 'med': 0.19999999999999996, 'far': 0.0}]
        list_memValues = []
        for i in range(len(self.inputs)):
            list_memValues.append(list_Values[i][self.inputs[i]])#iterrate over list ie first dictionary and second and pulls the value of [self.inputs[i] string from first and second dictionary. Strings are the keys
        return min(list_memValues)


#            RULEBASE

#             input i           output O
#            [RFS  RBS]       [ TURNING, SPEED]
r1 = rule(['close', 'close'], ['left', 'slow'])
r2 = rule(['close', 'med'], ['left', 'slow'])
r3 = rule(['close', 'far'], ['left', 'med'])
r4 = rule(['med', 'close'], ['right', 'med'])
r5 = rule(['med', 'med'], ['med', 'med'])
r6 = rule(['med', 'far'], ['left', 'med'])
r7 = rule(['far', 'close'], ['right', 'slow'])
r8 = rule(['far', 'med'], ['right', 'slow'])
r9 = rule(['far', 'far'], ['right', 'slow'])


#Tried to implement Front sensor, Left front sensor and right front sensor 'front2': find_nearest(msg.ranges[355:360])
# 'fright': find_nearest(msg.ranges[310:320]),'fleft': find_nearest(msg.ranges[40:50]) However it did not worked


#          [FS       LFS      RFS]    [ TURNING, SPEED]
'''r1 = rule(['close', 'close','close'], ['right', 'slow'])
r2 = rule(['close','close' , 'med'],   ['right', 'slow'])
r3 = rule(['close','close' , 'far'],   ['right', 'med'])
r4 = rule(['far' , 'close' , 'far'],   ['right', 'slow'])
r5 = rule(['close', 'med' , 'far'],     ['right', 'med'])
r6 = rule(['close', 'far' ,'med'],     ['left', 'slow'])
r7 = rule(['close' ,'far' ,'far'],   ['right', 'slow'])
r8 = rule(['close', 'med' ,'med'],     ['right', 'slow'])
r9 = rule(['med', 'close' , 'med'],     ['right', 'slow'])

r10 = rule(['close', 'med' , 'close'], ['left', 'slow'])
r11 = rule(['close','far','close'], ['left', 'slow'])
r12 = rule(['med', 'med' ,'med'],   ['med', 'med'])
r13 = rule(['med', 'med','close'],   ['left', 'med'])
r14 = rule(['med', 'med','far'],   ['right', 'med'])
r15 = rule(['med', 'far','far'],     ['left', 'slow'])
r16 = rule(['med', 'close' ,'close'],     ['med', 'slow'])
r17 = rule(['med', 'far', 'close'],   ['left', 'slow'])
r18 = rule(['med', 'close' ,'far'],     ['med', 'slow'])
r19 = rule(['far', 'far' ,'far'],     ['med', 'med'])

r20 = rule(['med', 'close' ,'med'], ['right', 'slow'])
r21 = rule(['far', 'far', 'close'],   ['left', 'med'])
r22 = rule(['far', 'far' 'med'],   ['med', 'med'])
r23 = rule(['far', 'med' ,'med'],   ['left', 'med'])
r24 = rule(['far', 'close' 'close'],   ['med', 'med'])
r25 = rule(['far', 'med' ,'close'],     ['left', 'med'])
r26 = rule(['far', 'close' ,'med'],     ['right', 'slow'])
r27 = rule(['far', 'med' ,'far'],   ['right', 'slow'])'''



# initaite the dictionary to store the string value assosiated with Close mid far (RBS = {}  and RFS = {})
# as keys and value of Key is membership value y
RBS = {}
RBS['close'] = close_RB_Dist.getMemberValue(RB_dist)
RBS['med'] = med_RB_Dist.getMemberValue(RB_dist)
RBS['far'] = far_RB_Dist.getMemberValue(RB_dist)
RFS = {}
RFS['close'] = close_RF_Dist.getMemberValue(RF_dist)
RFS['med'] = med_RF_Dist.getMemberValue(RF_dist)
RFS['far'] = far_RF_Dist.getMemberValue(RF_dist)
list_Values = [RFS, RBS]


#Determine all rule firing strength some will have firing strength zero other will have vlaue so nine
#element of the list startting with rule 1 and emd at 9. so value at rulebase[0] is fire rule firing value
rulebase = [r1.getFir(list_Values), r2.getFir(list_Values), r3.getFir(list_Values), r4.getFir(list_Values),
            r5.getFir(list_Values), r6.getFir(list_Values), r7.getFir(list_Values), r8.getFir(list_Values),
            r9.getFir(list_Values)]

turn_out = [1, -1, -1, 1, 0, -1, 1, 1, 0]
vel_out = [0, 0, 0, 0, 0.5, 0.5, 0, 0.5, 0.5]

firing_strengths = []
vel = []
turn = []
for i in range(len(rulebase)):
    if rulebase[i] > 0:  # firing strenght > 0 that means that rule is firing
        firing_strengths.append(rulebase[i])
        vel.append(vel_out[i])      #velocity against that rule from list vel_out
        turn.append(turn_out[i])    #turning against that rule from list turn_out

class rulebase:

    def __init__(self, rules):
        self.rules = rules

#defizification
    def Defuz(self, firing_strengths, turn, vel):

        speed = []
        for i in range(len(firing_strengths)):
            a = firing_strengths[i] * vel[i]
            speed.append(a)
        speed = sum(speed) / sum(firing_strengths)

        turning = []
        for i in range(len(firing_strengths)):
            b = firing_strengths[i] * turn[i]
            turning.append(b)
        turning = sum(turning) / sum(firing_strengths)

        return (speed, turning)


r_b = rulebase([])

velocity, turning = r_b.Defuz(firing_strengths, turn, vel)


print('\nvelocity {}\nturning {}'.format(velocity, turning))

mynode_ = None
pub_ = None
regions_ = {
    'right': 0,
    'fright': 0,
    'front1': 0,
    'front2': 0,
    'fleft': 0,
    'left': 0,
}
twstmsg_ = None


# main function attached to timer callback
def timer_callback():
    global pub_, twstmsg_
    if twstmsg_ is not None:
        pub_.publish(twstmsg_)

def clbk_laser(msg):
    global regions_, twstmsg_

    regions_ = {
        'front1': find_nearest(msg.ranges[0:5]),
        'front2': find_nearest(msg.ranges[355:360]),
        'right': find_nearest(msg.ranges[265:275]),
        'fright': find_nearest(msg.ranges[310:320]),
        'fleft': find_nearest(msg.ranges[40:50]),
        'left': find_nearest(msg.ranges[85:95])
    }
    twstmsg_ = movement()

def find_nearest(lst):
    f_list = filter(lambda item: item > 0.0, lst)
    return min(min(f_list, default=10), 10)

def movement():
    global twstmsg_
    fuzzy_instance = Fuzzyobstacleavoidance(regions_['fright'], regions_['right']) #iniate the Fuzzylogic controller with FRS and front back sensor
    x, y = fuzzy_instance
    msg = Twist()
    # If an obstacle is found to be within 0.25 of the LiDAR sensors front region, the fuzzy controller is used
    if regions_['front1'] < 0.25:
        msg.linear.x = 0.0
        msg.angular.z = 0.0
    else:
        msg.linear.x = x
        msg.angular.z = y
    return msg


def stop():
    global pub_
    msg = Twist()
    msg.angular.z = 0.0
    msg.linear.x = 0.0
    pub_.publish(msg)

def main():
    global pub_, mynode_global

    rclpy.init()
    mynode_ = rclpy.create_node('reading_laser')

    qos = QoSProfile(
        depth=10,
        reliability=ReliabilityPolicy.BEST_EFFORT,
    )

    pub_ = mynode_.create_publisher(Twist, '/cmd_vel', 10)
    sub = mynode_.create_subscription(LaserScan, '/scan', clbk_laser, qos)
    timer_period = 0.2
    timer = mynode_.create_timer(timer_period, timer_callback)

    try:
        rclpy.spin(mynode_)
    except KeyboardInterrupt:
        stop()
    except:
        stop()
    finally:
        mynode_.destroy_timer(timer)
        mynode_.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()






