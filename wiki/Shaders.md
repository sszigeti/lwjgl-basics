##### [start](https://github.com/mattdesl/lwjgl-basics/wiki) » Shaders
***

## Contents 

  * [Intro](#Intro)
  * [Lesson 1](ShaderLesson1) covers the basics of writing your own vertex and fragment shaders.
  * [Lesson 2](ShaderLesson2) covers texture sampling and basic image processing (inverting a texture).
  * [Lesson 3](ShaderLesson3) covers vignettes, circles, grayscale, and sepia effects.
  * [Lesson 4](ShaderLesson4) briefly introduces multiple texture units and "texture splatting."
  * [Lesson 5](ShaderLesson5) introduces a two-pass gaussian blur.
    * [Blurs for Mobile Applications in LibGDX](OpenGL-ES-Blurs)
  * [Lesson 6](ShaderLesson6) covers normal map lighting for 2D games. 


<a name="Intro" />
## Intro

GLSL stands for OpenGL Shading Language. Shaders are like small scripts that let us interact with the graphics processor more closely. They are an essential aspect of graphics programming, and can be used for a variety of effects and visuals in your 2D and 3D games. For now, there are two types of shaders you should familiarize yourself with:

### Vertex Shaders

As discussed in the [Textures](https://github.com/mattdesl/lwjgl-basics/wiki/Textures) article, a **vertex** is a point in space with some attributes attached to it, like position (xyz), colour (rgba), texture coordinates (st). A “vertex shader” allows you to interact with this vertex information before sending it along the graphics pipeline to be rendered.

Vertex shaders are often more applicable in 3D graphics programming -- e.g. applying a noise displacement to the vertices of a 3D mesh -- but they are still essential to understand even for 2D games.

### Fragment Shaders

Often called “pixel shaders,” these allow us to modify individual pixels before they are sent along the graphics pipeline. These shaders “output” a RGBA colour. Think of it like a return statement: if we rendered a sprite with a fragment shader that only returned the colour red `(R=1, G=0, B=0, A=1)` – the result would be a red box! 

### Basic Shaders

Vertex and fragment shaders both require a `main()` method. Vertex shaders typically pass the position of the vertex on to GL, like so:

```glsl
//the position of the vertex as specified by our renderer
attribute vec3 Position;

void main() {
    //pass along the position
    gl_Position = vec4(Position, 1.0);
}
```

Whereas fragment shaders typically pass the frag color (i.e. "pixel" color) along, like so:
```glsl
void main() {
    //pass along the color red
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
```

## On to Lesson 1

Check out [Lesson 1](ShaderLesson1) to get started.

## Further Reading

The best way to learn GLSL is through experimentation and practice. Once you've finished the lessons, check out some online GLSL effects to see how they were achieved:

- http://glsl.heroku.com/
- http://www.shadertoy.com

If you're feeling comfortable with GLSL, you could also try making your own shader-based sprite batcher (see [here](https://github.com/mattdesl/lwjgl-basics/wiki/ShaderProgram-Utility) and [here](https://github.com/mattdesl/lwjgl-basics/wiki/SpriteBatch)) in order to have a better grasp of how it all comes together.

## Shaders on Mobile and Embedded Systems

OpenGL ES 2.0 also supports GLSL. Generally you need to be even more careful when using GLSL on iOS and Android, as there are some performance and compiler considerations to be aware of. You can read about them [here](GLSL-Gotchas).

## GLSL Version Differences

There are some syntax differences between different GLSL versions. You can read about them [here](GLSL-Versions).