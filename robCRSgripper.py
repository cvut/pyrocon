
def robCRSgripper(self, commander, power):

    b = commander.robot.gripper_bounds
    f = commander.robot.gripper_bounds_force

    if (abs(power) <= 0.1): # 'position' mode
     pos = ((0.1 - power) * b(1) + (power - 0.1) * b(2) + 0.1) / 0.2

    else: # 'force' mode
     # the force is simulated such that we set the position otside
     #  the physical range and the force is generated by P component of
     #  PID regulator(the I component must be definitely set to 0!)

     if (power > 0): # set pos between b(2) and f(2)
      pos = ((1 - power) * b(2) + (power - 0.1) * f(2)) / 0.9
     else: # set pos between b(1) and f(1) power = -power
      pos = ((1 - power) * b(1) + (power - 0.1) * f(1)) / 0.9

    # Release errors and reset controller
     commander.rcon.write('RELEASE%s:' % commander.robot.gripper_ax)

    # Set position on gripper
     commander.rcon.write('G%s:%d' % (commander.robot.gripper_ax, pos))

    # Release motor of open gripper
    if (power == 0):
     commander.wait_gripper_ready() #, pos )
     commander.rcon.write('RELEASE%s:' % commander.robot.gripper_ax)



def robCRSgripperinit(controller):
    m = controller.robot.gripper_ax
    # Set  analog  mode  of controller
    controller.rcon.write('ANAXSETUP%s:%i,%i' %(m, controller.robot.gripper_ADC, controller.robot.gripper_current))
    
    # Maximal  curent  limit(0 - 255)
    controller.rcon.write('REGS1%s:%i' % (m, controller.robot.gripper_current))
    
    # Limitation  constant(feedback  from overcurrent)
    controller.rcon.write('REGS2%s:%i' % (m, controller.robot.gripper_feedback))
    
    # Maximal  energy  limits  voltage  on  motor
    controller.rcon.write('REGME%s:%i' % (m, controller.robot.gripper_REGME))
    
    # Maximal  speed
    controller.rcon.write('REGMS%s:%i' % (m, controller.robot.gripper_REGMS))
    
    # Axis  configuration  word
    controller.rcon.write('REGCFG%s:%i' % (m, controller.robot.gripper_REGCFG))
    
    # PID  parameters  of  controller
    controller.rcon.write('REGP%s:%i' % (m, controller.robot.gripper_REGP))
    controller.rcon.write('REGI%s:%i' % (m, controller.robot.gripper_REGI))
    controller.rcon.write('REGD%s:%i' % (m, controller.robot.gripper_REGD))