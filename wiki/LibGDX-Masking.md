# Clipping

Rendering a sprite masked by a rectangle is dead simple in LibGDX and OpenGL. We simply draw a TextureRegion to our SpriteBatch, which acts as a sub-region of a texture:
```java
TextureRegion myRegion;

 ... create
    myRegion = new TextureRegion(texture, x, y, width, height);

 ... render    
    batch.draw(myRegion, x, y);
```

To mask a series of overlapping sprites, such as a GUI element that may contain some text, we can use glScissor and `SCISSOR_TEST`. It looks like this, assuming we are using the standard y-up coordinate system:

```java
Gdx.gl.glEnable(GL10.GL_SCISSOR_TEST);
Gdx.gl.glScissor(clipX, clipY, clipWidth, clipHeight);

batch.begin();
//draw sprites to be clipped
batch.draw(sprite, 0, 0, 250, 250);
batch.end();

Gdx.gl.glDisable(GL10.GL_SCISSOR_TEST);
```

Note that we need to `end()` the batch before disabling scissor testing. Another approach is to call `flush()` on the SpriteBatch, which forces the data to be sent to GL. This allows us to, say, have the following flow:

```java
batch.begin();

//draw sprites
batch.draw(...);

//flush with current GL states
batch.flush();

//now we can change the GL state for future rendering...
Gdx.gl.glXXXXXXX(...);

//continue drawing
batch.draw(...);

//end the batch once we're all finished
batch.end();
```

Sometimes it can be a bit faster to just flush a batch, rather than calling `end()` followed by `start()`.

# Complex Masks

Masking something other than an axis-aligned rectangle becomes a little bit more difficult. Here are some common approaches.

### Masking in Software

This is the approach taken by frameworks like Java2D and other high-level 2D renderers. The idea here is to apply the mask in software, by manipulating the RGBA data of a Pixmap, and then send the new pixels to the GPU through `Texture.drawPixmap`. This is an ideal solution for a scene that does not need to be rendered or updated frequently, as it allows full control over each pixel; however, it is not suitable for real-time use, especially not on Android or iOS. We won't discuss this in much detail here, but if you are interested the [LibGDX Textures](LibGDX-Textures) tutorial would be a good place to start.

### Masking with Stencil Buffer

An old-school technique in OpenGL for masking is to use the stencil buffer. The basic idea is to render your primitives (such as those created by ShapeRenderer) to the stencil buffer, then render your scene with stencil buffer testing enabled to apply the clipping. The downside is that you lose anti-aliasing (such as a smooth edge to a circle).

If you choose this route, make sure to enable the stencil buffer with `AndroidApplicationConfiguration.stencil` (e.g. set it to 8 bits). 

### Masking with Depth Buffer

Another approach is to use the depth buffer to discard pixels in hardware. We first clear the depth buffer with a value of 1.0. Then, we render our shapes at `z=0`, using a depth function of `GL_LESS`. We can imagine it like so: each pixel in the depth buffer is 1.0, except the shapes we rendered (at depth 0.0), which "pass" the depth test because they are less than 1.0. In this step, we didn't write any colour information.

Then, we render our color sprites to the screen with the depth function `GL_EQUAL`, again at `z=0`. The result is that the fragment will pass the depth test (and be shown on screen) only if the z-value is equal to the value stored in the depth buffer.

You can see an example here:  
https://gist.github.com/mattdesl/6076849

<sup>Download the grass image [here](http://i.imgur.com/oODzehT.png) and save it as `grass.png` in your *assets/data* folder.</sup>

The advantage of this is that fragments outside of our masked areas will be discarded from the OpenGL pipeline, allowing for a significant performance boost (especially on fill-limited devices like Android/iOS). 

The downside, as with stencil buffer, is that we don't have a smooth alpha blending that you might expect from a circular mask.

Ideally you should always try to batch your rendering where possible; so if you have many masks to apply to a single scene, it would be better to draw all the mask shapes at once to the depth buffer. 

### Masking with Blend Functions

Another common approach is to use blend functions to achieve masking. The benefit of this is that it can lead to smooth alpha-blending, such as a feathered circle. The major downsides is that it does not discard pixels outside of the mask, and also the nature of the blending may introduce some more fill-rate issues. It also does not scale well, since we are dealing with raster and not vector information. Further, there have been some reported issues with these blend functions on [certain Android devices](http://www.badlogicgames.com/forum/viewtopic.php?p=44987#p44987). 

Again, standard batching applies. Try your best to render all your masks in one go, and then all your tiles/sprites in another go. The less you are flushing batches, the better your performance will be.

You can see an example here:  
https://gist.github.com/mattdesl/6076846

<sup>Download the mask image [here](http://i.imgur.com/PMkKLuP.png) and save it as `mask.png` in your *assets/data* folder.</sup>

### Fragment Shader with gl_FragCoord

Other approaches to masking might utilize a fragment shader. 
---- TODO

### Fragment Shader with Multi-Texture

Another shader approach is to use two textures in a single draw call, and apply the blending or masking in the fragment shader. The primary downsides is that you will probably require a second set of texture coordinates passed to the vertex shader (which SpriteBatch doesn't support, at the moment), and that you will want your textures to be the same size for best results.

However, for complex masks, especially dynamic masks that might be changing, this might be a good option. See here:  
https://github.com/mattdesl/lwjgl-basics/wiki/ShaderLesson4

### Fragment Shader with Custom Attributes

... TODO

### Textured Mesh

We can use LibGDX meshes to construct arbitrary shapes for us, and supply texture coordinates to each vertex. If we calculate the texture coordinates correctly, it will lead to a desirable masking. This means we can use arbitrary polygons, lines, etc. as our masks, adjusting them in real-time without much of a performance hit. It also paves the way for other features, such as tiling a texture across the polygon. 

This is a good solution but, like the others which rely on GL primitives, we lose anti-aliasing along the edges. For certain shapes, like circles and lines, this can be fixed by providing hints for anti-aliasing as vertex attributes.

---- TODO

## Notes

- Anti-aliasing is enabled by default in WebGL, at least in major browsers like Chrome and Firefox
- Remember to flush() or end your batch before changing GL states. This includes things like setting the blend and depth functions and enabling/disabling a GL state.
- Fill-rate is limited on Android and iOS, so it might be beneficial to use a combination of multiple techniques, such as shader and depth masking.