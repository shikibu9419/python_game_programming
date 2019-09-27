""" tiny_2d.py - tiny 2d physics engine - Copyright 2016 Kenichiro Tanaka """
from math import hypot

SHAPE_CIRCLE = 3
SHAPE_RECTANGLE = 4
SHAPE_LINE = 5

class Vec():
    """ 2d vector """
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos

    def add(self, vec):
        """ add a vector """
        return Vec(self.xpos + vec.xpos, self.ypos + vec.ypos)

    def mul(self, xscale, yscale):
        """ multiply a vector """
        return Vec(self.xpos * xscale, self.ypos * yscale)

    def dot(self, vec):
        """ inner dot """
        return self.xpos * vec.xpos + self.ypos * vec.ypos

    def cross(self, vec):
        """ cross product """
        return self.xpos * vec.ypos - vec.xpos * self.ypos

    def move(self, diffx, diffy):
        """ translate this vector """
        self.xpos += diffx
        self.ypos += diffy

class RectangleEntity():
    """ Rectangle object for tiny_2d """
    def __init__(self, xpos, ypos, width, height):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.shape = SHAPE_RECTANGLE
        self.fixed = True
        self.deceleration = 1.0

    def is_hit(self, xpos, ypos):
        """ if the point is included in the rectangle """
        return self.xpos <= xpos <= self.xpos + self.width and \
            self.ypos <= ypos <= self.ypos + self.height

class LineEntity():
    """ Line object for tiny_2d """
    def __init__(self, xpos0, ypos0, xpos1, ypos1,
                 restitution=0.9):
        self.shape = SHAPE_LINE
        self.fixed = True
        self.xpos = (xpos0 + xpos1) / 2
        self.ypos = (ypos0 + ypos1) / 2
        self.pos0 = (xpos0, ypos0)
        self.pos1 = (xpos1, ypos1)
        self.restitution = restitution
        self.vec = Vec(xpos1 - xpos0, ypos1 - ypos0)
        scale = 1 / hypot(self.vec.xpos, self.vec.ypos)
        self.norm = Vec(ypos0 - ypos1,
                        xpos1 - xpos0).mul(scale, scale)

class CircleEntity():
    """ Circle object for tiny_2d """
    def __init__(self, xpos, ypos, radius, fixed=False,
                 restitution=0.9, deceleration=1.0):
        self.shape = SHAPE_CIRCLE
        self.fixed = fixed
        self.xpos = xpos
        self.ypos = ypos
        self.radius = radius
        self.restitution = restitution
        self.deceleration = deceleration
        self.accel = Vec(0, 0)
        self.velocity = Vec(0, 0)

    def move(self, diffx, diffy):
        """ translate this object """
        self.xpos += diffx
        self.ypos += diffy

    def is_hit(self, xpos, ypos):
        """ return if xpos & ypos is inside of this """
        distance = hypot(xpos - self.xpos, ypos - self.ypos)
        return distance < self.radius

    def onhit(self, rect):
        """ who wants to recieve callback should override this """
        pass

    def collided_with_rect(self, rect):
        """ handle if this circle collided with a rectangle """
        nearx = max(rect.xpos, min(self.xpos,
                                   rect.xpos + rect.width))
        neary = max(rect.ypos, min(self.ypos,
                                   rect.ypos + rect.height))
        if not self.is_hit(nearx, neary):
            return

        self.onhit(rect)

        distance = hypot(nearx - self.xpos, neary - self.ypos)
        overlap = self.radius - distance
        movex, movey = 0, 0

        if neary == rect.ypos:
            movey = -overlap
        elif neary == rect.ypos + rect.height:
            movey = overlap
        elif nearx == rect.xpos:
            movex = -overlap
        elif nearx == rect.xpos + rect.width:
            movex = overlap
        else:
            movex = -self.velocity.xpos
            movey = -self.velocity.ypos

        self.move(movex, movey)

        if movex != 0:
            self.velocity = self.velocity.mul(-self.restitution, 1)
        if movey != 0:
            self.velocity = self.velocity.mul(1, -self.restitution)

    def collided_with_line(self, line):
        """ handle if this circle collided with a line """
        vec0 = Vec(line.pos0[0] - self.xpos + self.velocity.xpos, \
                line.pos0[1] - self.ypos + self.velocity.ypos)
        vec1 = self.velocity
        vec2 = Vec(line.pos1[0] - line.pos0[0],
                   line.pos1[1] - line.pos0[1])
        cv1v2 = vec1.cross(vec2)
        tv1 = vec0.cross(vec1) / cv1v2
        tv2 = vec0.cross(vec2) / cv1v2

        if 0 <= tv1 <= 1 and 0 <= tv2 <= 1:
            self.move(-self.velocity.xpos, -self.velocity.ypos)
            dot0 = self.velocity.dot(line.norm)
            vec0 = line.norm.mul(-2*dot0, -2*dot0)
            self.velocity = vec0.add(self.velocity)
            self.velocity = self.velocity.mul(
                line.restitution * self.restitution, \
                line.restitution * self.restitution)

    def collided_with_circle(self, peer):
        """ handle if this circle collided with a circle """
        distance = hypot(peer.xpos - self.xpos,
                         peer.ypos - self.ypos)
        if distance > self.radius + peer.radius:
            return

        self.onhit(peer)
        peer.onhit(self)

        distance = 0.01 if distance == 0 else distance
        overlap = self.radius + peer.radius - distance

        vec = Vec(self.xpos - peer.xpos, self.ypos - peer.ypos)
        a_norm = vec.mul(1 / distance, 1 / distance)
        b_norm = a_norm.mul(-1, -1)

        if not self.fixed and peer.fixed:
            self.move(a_norm.xpos * overlap, a_norm.ypos * overlap)
            dot0 = self.velocity.dot(a_norm)
            vec0 = a_norm.mul(-2 * dot0, -2 * dot0)
            self.velocity = vec0.add(self.velocity)
            self.velocity = self.velocity.mul(
                self.restitution, self.restitution)
        elif not peer.fixed and self.fixed:
            peer.move(b_norm.xpos * overlap, b_norm.ypos * overlap)
            dot1 = peer.velocity.dot(b_norm)
            vec1 = b_norm.mul(-2 * dot1, -2 * dot1)
            peer.velocity = vec1.add(peer.velocity)
            peer.velocity = peer.velocity.mul(
                peer.restitution, peer.restitution)
        else:
            self.move(a_norm.xpos * overlap / 2,
                      a_norm.ypos * overlap / 2)
            peer.move(b_norm.xpos * overlap / 2,
                      b_norm.ypos * overlap / 2)

            a_tang = Vec(a_norm.ypos * -1, a_norm.xpos)
            b_tang = Vec(b_norm.ypos * -1, b_norm.xpos)

            a_norm_scale, a_tang_scale = (a_norm.dot(self.velocity),
                                          a_tang.dot(self.velocity))
            b_norm_scale, b_tang_scale = (b_norm.dot(peer.velocity),
                                          b_tang.dot(peer.velocity))
            a_norm = a_norm.mul(a_norm_scale, a_norm_scale)
            a_tang = a_tang.mul(a_tang_scale, a_tang_scale)
            b_norm = b_norm.mul(b_norm_scale, b_norm_scale)
            b_tang = b_tang.mul(b_tang_scale, b_tang_scale)

            self.velocity = Vec(b_norm.xpos + a_tang.xpos,
                                b_norm.ypos + a_tang.ypos)
            peer.velocity = Vec(a_norm.xpos + b_tang.xpos,
                                a_norm.ypos + b_tang.ypos)

class Engine():
    """ tiny_2d engine object """
    def __init__(self, xpos=0, ypos=0, width=1000, height=1000,
                 gravity_x=0, gravity_y=0):
        self.world_x = xpos
        self.world_y = ypos
        self.world_w = width
        self.world_h = height
        self.gravity = Vec(gravity_x, gravity_y)
        self.entities = []

    def set_gravity(self, gravity_x, gravity_y):
        """ set gravity """
        self.gravity = Vec(gravity_x, gravity_y)

    def step(self, elapsed):
        """ move the clock tick a step forward """
        grav = self.gravity.mul(elapsed, elapsed)
        entities = self.entities

        for entity in entities:
            if not entity.fixed:
                accel = entity.accel.mul(elapsed, elapsed)
                entity.velocity = entity.velocity.add(grav)
                entity.velocity = entity.velocity.add(accel)
                entity.velocity = entity.velocity.mul(
                    entity.deceleration, entity.deceleration)
                entity.move(entity.velocity.xpos, entity.velocity.ypos)

        self.entities = list(filter(lambda e: \
            self.world_x <= e.xpos <= self.world_x + self.world_w and \
            self.world_y <= e.ypos <= self.world_y + self.world_h, entities))

        for ipos in range(len(entities) - 1):
            for jpos in range(ipos + 1, len(entities), 1):
                ent0, ent1 = entities[ipos], entities[jpos]
                if ent0.fixed and ent1.fixed:
                    continue

                if ent0.shape == SHAPE_CIRCLE and\
                   ent1.shape == SHAPE_CIRCLE:
                    ent0.collided_with_circle(ent1)
                elif ent0.shape == SHAPE_CIRCLE and\
                     ent1.shape == SHAPE_LINE:
                    ent0.collided_with_line(ent1)
                elif ent0.shape == SHAPE_LINE and\
                     ent1.shape == SHAPE_CIRCLE:
                    ent1.collided_with_line(ent0)
                elif ent0.shape == SHAPE_CIRCLE and\
                     ent1.shape == SHAPE_RECTANGLE:
                    ent0.collided_with_rect(ent1)
                elif ent0.shape == SHAPE_RECTANGLE and\
                     ent1.shape == SHAPE_CIRCLE:
                    ent1.collided_with_rect(ent0)
