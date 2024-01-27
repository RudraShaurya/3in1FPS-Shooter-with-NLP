import random
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.health_bar import HealthBar
from settings import *
from NLP import genre
# genre = 'fantasy'

app = Ursina()

Entity.default_shader = lit_with_shadows_shader

skybox = Entity(model='sky_dome', texture=models[genre]['background']['texture'], scale=500, double_sided=True)
ground = Entity(model='plane', collider='box', scale=SIZE, texture=models[genre]['ground']['texture'],
                color=models[genre]['ground']['color'], texture_scale=(4, 4))

score = 0
score_text = Text(text='Score: '+str(score), color=color.cyan, x=-0.89, y=0.5)

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.dark_gray, origin_y=-.5, speed=BASE_SPEED)
player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))

gun = Entity(model='cube', parent=camera, position=(.5, -.25, .25), scale=(.3, .2, 1), origin_z=-.5, color=color.red,
             on_cooldown=False)
gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)

shootables_parent = Entity()
mouse.traverse_target = shootables_parent


for i in range(256):
    Entity(model=models[genre]['building']['model'], origin_y=0, scale=models[genre]['building']['scale'],
           texture=models[genre]['building']['texture'],
           x=random.uniform(-((SIZE/2)-2), ((SIZE/2)-2)),
           z=random.uniform(-((SIZE/2)-2), ((SIZE/2)-2)),
           collider='cylinder',
           color=models[genre]['building']['color']
           )

    if i < 128 and genre == 'horror':
        Entity(model="cube", collider="box",
               x=random.uniform(-((SIZE/2)-2), ((SIZE/2)-2)),
               z=random.uniform(-((SIZE/2)-2), ((SIZE/2)-2)),
               rotation=(0, random.uniform(0, 90), 0),
               scale=(15, 10, 1), color=color.black)


def update():
    global score_text, score
    if held_keys['left mouse']:
        shoot()
    if held_keys['left shift']:
        player.speed = 2*BASE_SPEED
    else:
        player.speed = BASE_SPEED

    score_text.text = 'Score: '+str(score)
    spawn_enemies()


def shoot():
    if not gun.on_cooldown:
        gun.on_cooldown = True
        gun.muzzle_flash.enabled=True
        from ursina.prefabs.ursfx import ursfx
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.2, wave='noise',
              pitch=random.uniform(-13, -12), pitch_change=-20, speed=1.0)
        invoke(gun.muzzle_flash.disable, delay=.05)
        invoke(setattr, gun, 'on_cooldown', False, delay=.15)
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            mouse.hovered_entity.hp -= 10
            mouse.hovered_entity.blink(color.red)


class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model=models[genre]['enemy']['model'], scale=5, origin_y=0,
                         texture=models[genre]['enemy']['texture'], color=models[genre]['enemy']['color'],
                         collider='cube', **kwargs)
        self.health_bar = Entity(parent=self, y=self.position.y+0.75, model='cube', color=color.red, world_scale=(1.5, .1, .1))
        self.max_hp = 100
        self.hp = self.max_hp

    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 40:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0, 1, 0), self.forward, 30, ignore=(self,))
        if hit_info.entity == player:
            if dist > 4:
                self.position += self.forward * time.dt * models[genre]['speed']

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        global score
        self._hp = value
        if value <= 0:
            destroy(self)
            enemies.remove(self)
            score += 1
            score_text.text = 'Score: ' + str(score)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1


# Enemy()
enemies = []


def spawn_enemies():
    if len(enemies) < ENEMY_COUNT:
        enemies.append(Enemy(x=random.randint(-((SIZE/2) - 8), ((SIZE/2) - 8)),
                             z=random.randint(-((SIZE/2) - 8), ((SIZE/2) - 8))))


def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        gun.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled


pause_handler = Entity(ignore_paused=True, input=pause_input)

spawn_enemies()
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
Sky()

app.run()
