
def robCRSgripper(commander, power):

    b = commander.robot.gripper_bounds
    f = commander.robot.gripper_bounds_force

    if (abs(power) <= 0.1): # 'position' mode
        pos = ((0.1 - power) * b[0] + (power - 0.1) * b[1] + 0.1) / 0.2

    else: # 'force' mode
     # the force is simulated such that we set the position otside
     #  the physical range and the force is generated by P component of
     #  PID regulator(the I component must be definitely set to 0!)

        if (power > 0): # set pos between b[1] and b[1]
            pos = ((1 - power) * b[1] + (power - 0.1) * b[1]) / 0.9
        else: # set pos between b[0] and b[0] power = -power
            pos = ((1 - power) * b[0] + (power - 0.1) * b[0]) / 0.9

        # Release errors and reset controller
        commander.rcon.write('RELEASE%s:\n' % commander.robot.gripper_ax)
        # Set position on gripper
        commander.rcon.write('G%s:%d\n' % (commander.robot.gripper_ax, pos))

    # Release motor of open gripper
    if (power == 0):
        commander.wait_gripper_ready() #, pos )
        commander.rcon.write('RELEASE%s:\n' % commander.robot.gripper_ax)



def robCRSgripperinit(controller):
    m = controller.robot.gripper_ax
    # Set  analog  mode  of controller
    controller.rcon.write('ANAXSETUP%s:%i,%i\n' %(m, controller.robot.gripper_ADC, controller.robot.gripper_current))

    # Maximal  curent  limit(0 - 255)
    controller.rcon.write('REGS1%s:%i\n' % (m, controller.robot.gripper_current))

    # Limitation  constant(feedback  from overcurrent)
    controller.rcon.write('REGS2%s:%i\n' % (m, controller.robot.gripper_feedback))

    # Maximal  energy  limits  voltage  on  motor
    controller.rcon.write('REGME%s:%i\n' % (m, controller.robot.gripper_REGME))

    # Maximal  speed
    controller.rcon.write('REGMS%s:%i\n' % (m, controller.robot.gripper_REGMS))

    # Axis  configuration  word
    controller.rcon.write('REGCFG%s:%i\n' % (m, controller.robot.gripper_REGCFG))

    # PID  parameters  of  controller
    controller.rcon.write('REGP%s:%i\n' % (m, controller.robot.gripper_REGP))
    controller.rcon.write('REGI%s:%i\n' % (m, controller.robot.gripper_REGI))
    controller.rcon.write('REGD%s:%i\n' % (m, controller.robot.gripper_REGD))
