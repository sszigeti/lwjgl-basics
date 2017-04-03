### OpenGL & GLSL Tutorials

These tutorials are specific to LWJGL devs. They use the lwjgl-basics API to reduce clutter and minimize GL boilerplate. Each of the [Shaders](wiki/Shaders) tutorials includes a LibGDX port.

* [Display Creation](wiki/Display) 
* [OpenGL Textures](wiki/Textures)
  * [Using Buffers with LWJGL](wiki/Java-NIO-Buffers)
* [Batching Sprites](wiki/Sprite-Batching)
  * [Batching Rectangles and Lines](wiki/Batching-Rectangles-and-Lines)
* [Frame Buffer Objects](wiki/FrameBufferObjects)
* [Intro to Shaders](wiki/Shaders)
  * [Lesson 1: Red Boxes](wiki/ShaderLesson1)
  * [Lesson 2: Inverting a Texture](wiki/ShaderLesson2)
  * [Lesson 3: Circles, vignette, sepia and grayscale effects](wiki/ShaderLesson3)
  * [Lesson 4: Multiple Texture Units](wiki/ShaderLesson4)
  * [Lesson 5: Gaussian Blurs](wiki/ShaderLesson5)
      * [Appendix: Blurs for Mobile Applications in LibGDX](wiki/OpenGL-ES-Blurs)
  * [Lesson 6: Normal Map Lighting for 2D Games](wiki/ShaderLesson6)
* 5. Creating Your own 2D Renderer
  * [ShaderProgram Utility](wiki/ShaderProgram-Utility)
  * [Sprite Batching](wiki/SpriteBatch)

### LibGDX Tutorials

  * [Intro to LibGDX Textures and Pixmaps](wiki/LibGDX-Textures)
  * [Creating a Fruit Ninja Style Swipe](wiki/LibGDX-Finger-Swipe)
  * [Blurs for Mobile Applications](wiki/OpenGL-ES-Blurs)
  * [2D Per-Pixel Shadows on the GPU](wiki/2D-Pixel-Perfect-Shadows)
  * [Mesh and ImmediateModeRenderer Tutorials](wiki/LibGDX-Meshes)
  * [Custom Sprite Batcher in LibGDX](wiki/Custom-Sprite-Batcher-in-LibGDX) (WIP)

### Code Snippets & Tips

* LibGDX
  * [Using Java2D For Advanced Shapes & Rasterization (Desktop)](wiki/LibGDX-&-Java2D)
  * [Rendering a Textured Triangle with SpriteBatch](https://gist.github.com/4255476)
  * [Hiding the Mouse Cursor (Desktop)](https://gist.github.com/4255483)
  * [Sprite Brightness/Contrast in GL11 and GL20](wiki/LibGDX-Brightness-&-Contrast)
* GLSL Sandbox
  * [Ray Marching Scene](http://glsl.heroku.com/e#14157.0)
  * [Outlined Circle](http://glsl.heroku.com/e#4635.0)
  * [Procedural Bricks](http://glsl.heroku.com/e#5215.13)
  * [Spotlight WIP](http://glsl.heroku.com/e#5700.4)
  * [Flying Lotus' Cosmogramma in Code (Album Artwork)](http://glsl.heroku.com/e#5928.5)
  * [Underwater](http://glsl.heroku.com/e#6052.4)
  * [Space](http://glsl.heroku.com/e#6607.3)
  * [Rotated 2D Rounded Rectangle](http://glsl.heroku.com/e#8013.4)
  * [Earth](http://glsl.heroku.com/e#7662.3)
* Misc
  * [2D Lightning Effect](wiki/LightningEffect)
  * [Tiled Maps from Images](wiki/Tiled-Map-Images)
  * [GLSL Gotchas](wiki/GLSL-Gotchas)

***

### The API

You can also use the *lwjgl-basics* source code as a minimal shader-based library for 2D LWJGL sprite games. It provides essential utilities for textures, shaders, and sprite rendering.

For a large game project, a platform like [LibGDX](http://libgdx.badlogicgames.com/) may be more suitable.

The [source code](https://github.com/mattdesl/lwjgl-basics) is hosted on GitHub.

### Installing the API

The best way to install the API is to use Eclipse and EGit (or another IDE with Git support) to pull the most recent source code. Included in the `lib` and `native` folder is a distribution of LWJGL 2.8.5, as well as an Eclipse project with class path set up for you. You can download newer versions of LWJGL from their [downloads page](http://lwjgl.org/download.php). 

Alternatively, you can download the full library as a ZIP:

![ZIP](wiki/images/Dkvp0.png)

Then, simply open the Eclipse project to start testing. Ensure your LWJGL JARs and natives have been set correctly in [Eclipse](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_Eclipse), [NetBeans](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_NetBeans) or [IntelliJ](http://www.lwjgl.org/wiki/index.php?title=Setting_Up_LWJGL_with_IntelliJ_IDEA), and include lwjgl-basics as a class library. lwjgl-basics also uses PNGDecoder.jar as a dependency, which can be downloaded [here](http://twl.l33tlabs.org/textureloader/).

See the [tests](https://github.com/mattdesl/lwjgl-basics/tree/master/test/mdesl/test) package to get started with some basic examples.