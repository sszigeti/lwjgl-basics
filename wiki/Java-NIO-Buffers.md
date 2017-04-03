##### [start](https://github.com/mattdesl/lwjgl-basics/wiki) » [Textures](Textures) » Buffers
***

This is a short introduction to Java NIO buffers, which are commonly used in LWJGL to handle GL data. For a more detailed look at buffers, [see here](http://tutorials.jenkov.com/java-nio/buffers.html).

### Intro
A buffer is simply a block of memory which holds some data. For our purposes, you can think of it as an array of elements. However, instead of random access (e.g. `array[i]`), Buffers read and write data relative to their current position. To demonstrate, let's say we wish to create a buffer which holds four bytes, and then read those bytes out. You would create it like so:
```java
//LWJGL includes utilities for easily creating buffers
ByteBuffer buffer = BufferUtils.createByteBuffer(4);

//"relative put" method, which places the byte and 
//then moves the position forward
buffer.put(a);
buffer.put(b);
buffer.put(c);
buffer.put(d);

//flip the position to reset the relative position to zero
buffer.flip();

//loop through all of the bytes that were written, using "relative get"
for (int i=0; i<buffer.limit(); i++) {
    System.out.println( buffer.get() );
}
```

To understand what's happening, let's compare it to a Java array:
```java
//creating the fixed-size array..
byte[] array = new byte[4];

//position starts at 0
int position = 0;

//using a relative "put", position inreases each time
array[position++] = a;
array[position++] = b;
array[position++] = c;
array[position++] = d;

//"flipping" our position/limit
int limit = position;
position = 0;

//printing our values
for (int i=0; i<limit; i++) {
    //using a relative "get", position inreases each time
    System.out.println( array[position++] );
}
```

The `capacity` of a buffer is similar to the length of an array; but as we can see from the above example, the `limit` of a buffer may not be equal to its capacity if we've only written a limited number of bytes.

For convenience, you can "chain" calls with get/put/etc. like so:
```java
buffer.put(a).put(b).put(c).put(d);
```

### Practical Usage

So how does this relate to LWJGL and OpenGL? There are two common ways you'll be using buffers: writing data to GL (i.e. uploading texture data to the GPU), or reading data from GL (i.e. reading texture data from the GPU, or getting a certain value from the driver).

Let's say we are creating a 1x1 blue RGBA texture, our buffer setup would look like this:

```java
int width = 1; //1 pixel wide
int height = 1; //1 pixel high
int bpp = 4; //4 bytes per pixel (RGBA)

//create our buffer
ByteBuffer buffer = BufferUtils.createByteBuffer(width * height * bpp);

//put the Red, Green, Blue, and Alpha bytes
buffer.put((byte)0x00).put((byte)0x00).put((byte)0xFF).put((byte)0xFF);

//flip the buffer !!! this needs to be done before it can be read by GL
buffer.flip();

//here is an example of sending data to GL... we will talk 
//more about this method in the Texture section
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 
             width, height, 0, GL_RGBA, 
             GL_UNSIGNED_BYTE, buffer);
```

Below is an example of getting data from GL:

```java
//create a new buffer with at least 16 elements
IntBuffer buffer = BufferUtils.createIntBuffer(16);

//this will call relative "put" with the max texture size,
//then continue "putting" zeros until the buffer's capacity is reached,
//then it will flip() our buffer
glGetInteger(GL_MAX_TEXTURE_SIZE, buffer);

//since our buffer is already flipped, our position will be zero...
//so we can go ahead and grab the first element
int maxSize = buffer.get();
```

As described [in the docs](http://www.khronos.org/opengles/documentation/opengles1_0/html/glGetInteger.html), `GL_MAX_TEXTURE_SIZE` will give us one value, but since glGetInteger can return up to 16 elements, LWJGL expects our buffer to have at least that as a capacity. Where possible, you should try to re-use buffers instead of always creating new ones.

Also note that LWJGL includes convenience methods for glGetInteger, glGenTextures, and various other calls. So the above code would actually be reduced to the following:

```java
int maxSize = glGetInteger(GL_MAX_TEXTURE_SIZE);
```

## Appendix: LibGDX

In [LibGDX](http://libgdx.badlogicgames.com/), buffers are used in the same manner. However, LibGDX includes its own buffer creation utility, which you would use instead of LWJGL's. So in LibGDX the above code may look like this:

```java
//uses LibGDX's BufferUtils class
IntBuffer buffer = BufferUtils.newIntBuffer(16);

//Gdx.gl -> "common" functions that appear in GL10 and GL20
//Gdx.gl20 -> GLES20 functions, is only non-null if Gdx.graphics.isGL20Available() (useGL20=true in app cfg)
//Gdx.gl10 -> GLES10 functions, will be null if Gdx.graphics.isGL20Available()
Gdx.gl.glGetInteger(GL_MAX_TEXTURE_SIZE, buffer);

int maxSize = buffer.get();
```

LibGDX's Pixmap utilities mean that we rarely need to work with buffers directly to manipulate pixel data.