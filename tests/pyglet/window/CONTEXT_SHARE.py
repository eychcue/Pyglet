#!/usr/bin/env python

'''Test that multiple windows share objects by default.

This test is non-interactive.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import unittest
from ctypes import *

import pyglet.window
from pyglet.GL.VERSION_1_1 import *

__noninteractive = True

class CONTEXT_SHARE(unittest.TestCase):
    def test_context_share_list(self):
        w1 = pyglet.window.create(200, 200)
        w1.switch_to()
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glLoadIdentity()
        glEndList()
        self.assertTrue(glIsList(list))

        w2 = pyglet.window.create(200, 200)
        w2.switch_to()
        self.assertTrue(glIsList(list))

        w1.close()
        w2.close()

    def test_context_noshare_list(self):
        w1 = pyglet.window.create(200, 200)
        w1.switch_to()
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glLoadIdentity()
        glEndList()
        self.assertTrue(glIsList(list))

        factory = pyglet.window.get_factory()
        factory.set_context_share(pyglet.window.CONTEXT_SHARE_NONE)
        factory.set_size(200, 200)
        w2 = factory.create_window()
        w2.switch_to()
        self.assertTrue(not glIsList(list))

        w1.close()
        w2.close()

    def test_context_share_texture(self):
        w1 = pyglet.window.create(200, 200)
        w1.switch_to()
        textures = c_uint()
        glGenTextures(1, byref(textures))
        texture = textures.value

        glBindTexture(GL_TEXTURE_2D, texture)
        data = (c_ubyte * 4)()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, data)
        self.assertTrue(glIsTexture(texture))

        w2 = pyglet.window.create(200, 200)
        w2.switch_to()
        self.assertTrue(glIsTexture(texture))

        glDeleteTextures(1, byref(textures))
        self.assertTrue(not glIsTexture(texture))

        w1.switch_to()
        self.assertTrue(not glIsTexture(texture))

        w1.close()
        w2.close()

if __name__ == '__main__':
    unittest.main()

