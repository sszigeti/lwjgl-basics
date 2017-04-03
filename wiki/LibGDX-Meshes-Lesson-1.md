##### [start](https://github.com/mattdesl/lwjgl-basics/wiki) » [LibGDX Meshes](LibGDX-Meshes) » Lesson 1

***

This tutorial is part of a series. Take a look at the [Introduction](LibGDX-Meshes) before you move on.

# Batching Triangles

You can follow along with the full source code here:  
[MeshTutorial1.java](https://gist.github.com/mattdesl/5793041)

## Vert & Frag Shaders

Let's say we want to render several triangles of different sizes and colours. The best way to do this is to use a `Position` attribute which holds the `(x, y)` components of each vertex, and a `Color` attribute which holds the `(r, g, b, a)` components. First, we need to construct a shader for our mesh.

Vertex shader:
```glsl
//our attributes
attribute vec2 a_position;
attribute vec4 a_color;

//our camera matrix
uniform mat4 u_projTrans;

//send the color out to the fragment shader
varying vec4 vColor;

void main() {
	vColor = a_color;
	gl_Position = u_projTrans * vec4(a_position.xy, 0.0, 1.0);
}
```

Fragment shader:
```glsl
#ifdef GL_ES
precision mediump float;
#endif

//input from vertex shader
varying vec4 vColor;

void main() {
	gl_FragColor = vColor;
}
```

## Mesh Creation

Then, we need to set up some constants and create a float[] array which we will re-use later. Keep in mind that a triangle takes three vertices.

```java
//Position attribute - (x, y) 
public static final int POSITION_COMPONENTS = 2;

//Color attribute - (r, g, b, a)
public static final int COLOR_COMPONENTS = 4;

//Total number of components for all attributes
public static final int NUM_COMPONENTS = POSITION_COMPONENTS + COLOR_COMPONENTS;

//The "size" (total number of floats) for a single triangle
public static final int PRIMITIVE_SIZE = 3 * NUM_COMPONENTS;

//The maximum number of triangles our mesh will hold
public static final int MAX_TRIS = 1;

//The maximum number of vertices our mesh will hold
public static final int MAX_VERTS = MAX_TRIS * 3;

//The array which holds all the data, interleaved like so:
//    x, y, r, g, b, a
//    x, y, r, g, b, a, 
//    x, y, r, g, b, a, 
//    ... etc ...
protected float[] verts = new float[MAX_VERTS * NUM_COMPONENTS];

//The current index that we are pushing triangles into the array
protected int idx = 0;

@Override
public void create() {
	mesh = new Mesh(true, MAX_VERTS, 0, 
			new VertexAttribute(Usage.Position, POSITION_COMPONENTS, "a_position"),
			new VertexAttribute(Usage.Color, COLOR_COMPONENTS, "a_color"));
	... 
}
```

Notice that the last argument to Mesh is a varargs of VertexAttribute. The order you specify them should match the order you will be placing your data into the vertex array. Their names (like "a_color") should match the attribute specified in the shader, as should their component count. If you specify a component count of 1, the attribute should be a `float`, 2 components should be `vec2`, etc.

## Pushing Vertex Data

Now, we need to specify a "draw" method. Just like a SpriteBatch, this won't send any data to OpenGL; instead, it will just update our vertices array if we have more room. Once we are finished placing all the triangles in the batch, *then* we can send the data in a single GL render call. This is much more efficient than making a render call for each triangle.

```java
void drawTriangle(float x, float y, float width, float height, Color color) {
	//we don't want to hit any index out of bounds exception...
	//so we need to flush the batch if we can't store any more verts
	if (idx==verts.length)
		flush();
	
	//now we push the vertex data into our array
	//we are assuming (0, 0) is lower left, and Y is up
	
	//bottom left vertex
	verts[idx++] = x; 			//Position(x, y) 
	verts[idx++] = y;
	verts[idx++] = color.r; 	//Color(r, g, b, a)
	verts[idx++] = color.g;
	verts[idx++] = color.b;
	verts[idx++] = color.a;
	
	//top left vertex
	verts[idx++] = x; 			//Position(x, y) 
	verts[idx++] = y + height;
	verts[idx++] = color.r; 	//Color(r, g, b, a)
	verts[idx++] = color.g;
	verts[idx++] = color.b;
	verts[idx++] = color.a;

	//bottom right vertex
	verts[idx++] = x + width;	 //Position(x, y) 
	verts[idx++] = y;
	verts[idx++] = color.r;		 //Color(r, g, b, a)
	verts[idx++] = color.g;
	verts[idx++] = color.b;
	verts[idx++] = color.a;
}
```

## Rendering The Triangle Batch

Now we need to specify our "render" or "flush" method, which pushes the data to GL in a single render call.

Notice that we use OrthographicCamera so that we can specify our positions in 2D screen space. This only needs to be sent to the shader whenever it changes (i.e. on screen resize), but the performance impact is not too significant even if we send it every frame.

```java
void flush() {
	//if we've already flushed
	if (idx==0)
		return;
	
	//sends our vertex data to the mesh
	mesh.setVertices(verts);
	
	//no need for depth...
	Gdx.gl.glDepthMask(false);
	
	//enable blending, for alpha
	Gdx.gl.glEnable(GL20.GL_BLEND);
	Gdx.gl.glBlendFunc(GL20.GL_SRC_ALPHA, GL20.GL_ONE_MINUS_SRC_ALPHA);
	
	//number of vertices we need to render
	int vertexCount = (idx/NUM_COMPONENTS);
	
	//update the camera with our Y-up coordiantes
	cam.setToOrtho(false, Gdx.graphics.getWidth(), Gdx.graphics.getHeight());
	
	//start the shader before setting any uniforms
	shader.begin();
	
	//update the projection matrix so our triangles are rendered in 2D
	shader.setUniformMatrix("u_projTrans", cam.combined);
	
	//render the mesh
	mesh.render(shader, GL20.GL_TRIANGLES, 0, vertexCount);
	
	shader.end();
	
	//re-enable depth to reset states to their default
	Gdx.gl.glDepthMask(true);
	
	//reset index to zero
	idx = 0;
}
```

## Using the Batch

Now, we can use the batch like so in our ApplicationListener:

```java
@Override
public void render() {
	Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT);
	
	//push a few triangles to the batch
	drawTriangle(10, 10, 40, 40, Color.RED);
	drawTriangle(50, 50, 70, 40, Color.BLUE);
	
	//this will render the above triangles to GL, using Mesh
	flush();
}
```

## Optimization: Packed Color Data

LibGDX includes an option to use packed color data, instead of sending four floats for a RGBA color. This leads to a bit of an optimization as you are sending less data to GL per frame; however, it comes with a slight loss of color precision. To use packed color data, you need to use 1 as your COLOR_COMPONENTS count, and specify the VertexAttribute like so:
```java
//now we just need one float to specify color in our vertex array
public static final int COLOR_COMPONENTS = 1; 

...
    //VertexAttribute still expects ColorPacked to have 4 components
    ... new VertexAttribute(Usage.ColorPacked, 4, "a_color") ...
```

Then, you will send data like this instead:
```java
float c = color.toFloatBits();
		
//bottom left vertex
verts[idx++] = x; 			 
verts[idx++] = y;
verts[idx++] = c;

//top left vertex
verts[idx++] = x; 			 
verts[idx++] = y + height;
verts[idx++] = c;
		
//bottom right vertex
verts[idx++] = x + width;	 
verts[idx++] = y;
verts[idx++] = c;
```

***

# Prototyping with ImmediateModeRenderer

Now that you understand the concepts of how meshes and vertices come together to form geometry, we can utilize LibGDX's ImmediateModeRenderer for some faster prototyping. This is a specialized utility which is good for un-indexed geometry that holds `Position(x, y, z)` and some other optional attributes: `Normal(x, y, z)`, `Color(r, g, b, a)`, and a variable number of `TexCoord(s, t)`. 

## Setting up the renderer

First, we need to set up the renderer. This will create a default shader for us that has the vertex attributes we specified in the constructor:

```java
    //normals=false, colors=true, numTexCoords=no texture info
    r = new ImmediateModeRenderer20(false, true, 0);
```

Normals are generally not needed for 2D rendering. Colors and texture coordinates are optional, and dependent on your needs. For our triangle renderer, we do need colors, but not texture coordinates. 

When rendering, we use it like so. Notice that it uses a `vec3` for position; we can just ignore the Z component.
```java
//passes the projection matrix to the camera
r.begin(camera.combined, GL20.GL_TRIANGLES);

...

//push our vertex data here...

//specify normals/colors/texcoords before vertex position
r.color(color.r, color.g, color.b, color.a);
r.vertex(x, y, 0);

r.color(color.r, color.g, color.b, color.a);
r.vertex(x, y+height, 0);

r.color(color.r, color.g, color.b, color.a);
r.vertex(x+width, y, 0);

...

//flush the renderer
r.end();
```

The ImmediateModeRenderer does not do any bounds checking, so you will have to do that yourself before sending new vertex data!

## Custom Shaders with ImmediateModeRenderer

If we wanted to specify a custom shader, it should be passed in the constructor. Other than `Position` being a vec3, the other thing worth noting is that it uses the constants in ShaderProgram for the attribute names:
```
POSITION_ATTRIBUTE = "a_position"
NORMAL_ATTRIBUTE = "a_normal"
COLOR_ATTRIBUTE = "a_color"
TEXCOORD_ATTRIBUTE = "a_texCoord" + N
```

The texture coordinate is appended with the index; so if we specified a single texCoord, its attribute name in the shader would be `a_texCoord0`. If we did not specify these attributes when constructing ImmediateModeRenderer, then you should not include them in your vertex shader.

The uniform for the projection matrix is named `u_projModelView` and the texture uniforms will be `u_samplerN` (again, where N is the index).

## GLES10 Support

If our renderer is straight-forward and doesn't need shaders or any custom vertex attributes, we can use ImmediateModeRenderer10 to abstract the rendering pipeline for both GLES10 and GLES20:

```java
ImmediateModeRenderer r;

...
    if (Gdx.graphics.isGL20Available()) 
        r = new ImmediateModeRenderer20(false, true, 1);
    else
        r = new ImmediateModeRenderer10();
```