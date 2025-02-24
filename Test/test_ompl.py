from pyrfuniverse.envs.base_env import RFUniverseBaseEnv
import pyrfuniverse.attributes as attr
try:
    import pyrfuniverse.attributes.omplmanager_attr as rfu_ompl
except ImportError:
    raise Exception('This feature requires ompl, see: https://github.com/ompl/ompl')

env = RFUniverseBaseEnv(assets=['franka_panda', 'Collider_Box', 'OmplManager'])

robot = env.InstanceObject(name='franka_panda', id=123456, attr_type=attr.ControllerAttr)
robot.EnabledNativeIK(False)
box1 = env.InstanceObject(name='Collider_Box', id=111111, attr_type=attr.ColliderAttr)
box1.SetTransform(position=[-0.5, 0.5, 0], scale=[0.2, 1, 0.2])
box2 = env.InstanceObject(name='Collider_Box', id=111112, attr_type=attr.ColliderAttr)
box2.SetTransform(position=[0.5, 0.5, 0], scale=[0.2, 1, 0.2])
env.step()

ompl_manager = env.InstanceObject(name='OmplManager', attr_type=attr.OmplManagerAttr)
ompl_manager.modify_robot(123456)
env.step()

start_state = [0.0, -45.0, 0.0, -135.0, 0.0, 90.0, 45.0]
# target_state = [ompl_manager.joint_upper_limit[j] * 0.9 for j in range(ompl_manager.joint_num)]
target_state = [6.042808, -35.73029, -128.298, -118.3777, -40.28789, 134.8007, -139.2552]

planner = rfu_ompl.RFUOMPL(ompl_manager, time_unit=5)

ompl_manager.set_state(start_state)
env.step(50)

ompl_manager.set_state(target_state)
env.step(50)

ompl_manager.set_state(start_state)
env.step(50)

env.SetTimeStep(0.001)
env.step()

is_sol, path = planner.plan_start_goal(start_state, target_state)

print(target_state)
print(path[-1])

env.SetTimeStep(0.02)
env.step()

while True:
    if is_sol:
        planner.execute(path)