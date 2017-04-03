Drawing arbitrary 2D lines in OpenGL and OpenGL ES can be a bit tricky. GL_LINES is not always reliable, nor is it flexible enough for most production-quality line rendering. Anti-aliasing and line width support varies greatly from one driver to the next. glLineStipple is deprecated, as is GL_LINE_SMOOTH.

The solution is to render lines as triangles or triangle strips, and apply the anti-aliasing in the fragment processing step. 

The guide should serve as an introduction to basic vector math, as well as learning LibGDX's mesh utilities. The same concepts could be applied to any OpenGL-based framework.

## The Path

A line is just a series of 2D or 3D points which create a path. We could use any growable array, but since we are using LibGDX we will use the Array<T> class which is easier on the garbage collector. Later on, we can extend the Path class to provide support for splines and curves.

## Debugging with ShapeRenderer

In LibGDX, we can use ShapeRenderer for line debugging. T