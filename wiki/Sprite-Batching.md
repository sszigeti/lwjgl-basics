##### [start](https://github.com/mattdesl/lwjgl-basics/wiki) » Sprite Batching
***

If we tried using `debugTexture` from the [Textures](Textures) tutorial to render all of our tiles and sprites, chances are we'd quickly run into performance problems. This is because we are only pushing one sprite at a time to the GPU. What we need is to "batch" many sprites into the same draw call; for this we use a SpriteBatch.

## Intro

As discussed in the [Textures](Textures) tutorial, a sprite is nothing more than a set of vertices that make up a rectangular shape. Each vertex contains a number of attributes that define it, such as:

- `Position(x, y)` - where the vertex lies on the screen 
- `TexCoord(s, t)` - what region of our Texture we want to render
- `Color(r, g, b, a)` - the vertex color, used to specify tinting or transparency

Most sprite batchers are fairly simple to use, and may look like this in your game:

```java
//called on game creation
public void create() {
    //create a single batcher we will use throughout our application
    spriteBatch = new SpriteBatch();
}

//called on frame render
public void render() {
    //prepare the batch for rendering
    spriteBatch.begin(); 

    //draw all of our sprites
    spriteBatch.draw(mySprite1, x, y);
    spriteBatch.draw(mySprite2, x, y);
    ...

    //end the batch, flushing the data to GPU
    spriteBatch.end();
}

//called when the display is resized
public void resize(int width, int height) {
    //notify the sprite batcher whenever the screen changes 
    spriteBatch.resize(width, height);
}
```

First we `begin()` the batch, we simply tells it that it's in "drawing mode" and calls `use()` on our shader program. Then, calling `spriteBatch.draw(...)` pushes the sprite's vertex information (position, texcoord, color) onto a very large stack. The vertices aren't passed to the GPU until one of the following occurs:

- The batch is forced to render with `end()` or another call that flushes the batch, like `flush()`
- The user tries drawing a sprite that uses a different Texture than the last one. The batch needs to be flushed and the new texture bound before we can continue.
- We have reached the capacity of our stack, so we need to flush to start over again

This is the basic idea behind a sprite batcher. As you can see, using many textures will lead to many draw calls (as the batch will need to flush for each new texture). This is why a texture atlas (AKA sprite sheet) is always recommended; it allows us to render many sprites in a single draw call.

The [lwjgl-basics](https://github.com/mattdesl/lwjgl-basics/) API includes a minimal [SpriteBatch](https://github.com/mattdesl/lwjgl-basics/blob/master/src/mdesl/graphics/SpriteBatch.java) implementation free to use -- it's modeled after the batcher in [LibGDX](http://libgdx.badlogicgames.com/).

## TextureRegion

As discussed, for best performance we should use a texture atlas, and draw regions of it (AKA sub-images) to make up our game's sprites. For this we have a utility class, [TextureRegion](https://github.com/mattdesl/lwjgl-basics/blob/master/src/mdesl/graphics/TextureRegion.java). It allows us to specify in pixels the upper left position `(x, y)` and size `(width, height)` of our sub-image. Let's take our earlier example, where we want to render the highlighted tile:

![VertexBreakdown](images/nwXUM.png)

We can get a TextureRegion of the tile with the following:
```java
//specify x, y, width, height of tile
region = new TextureRegion(64, 64, 64, 64);
```

As you can see, the TextureRegion utility allows us to get sub-images without worrying about calculating the texture coordinates. We can then render the individual tile with our sprite batch like so:
```java
... inside SpriteBatch begin / end ...
spriteBatch.draw(region, x, y);
```

## Vertex Color

We can change the tinting and transparency of our sprites by adjusting the batch color, AKA "vertex color." 

The resulting RGB is multiplied by the texture color; so if we used a white texture `(1, 1, 1, 1)` and we specified a vertex color of `(1, 0, 0, 1)`, the result would be red. The Alpha component of the color allows us to adjust the opacity of sprites rendered to screen.

```java
spriteBatch.begin();

//draw calls will now use 50% opacity
spriteBatch.setColor(1f, 1f, 1f, 0.5f);
spriteBatch.draw(...);
spriteBatch.draw(...);

//draw calls will now use 100% opacity (default)
spriteBatch.setColor(1f, 1f, 1f, 1f);
spriteBatch.draw(...);

spriteBatch.end();
```

## Triangles, not Quads!

In the earlier series, we have been thinking of textures as quads, but in reality most sprite batchers will use two adjacent triangles to represent a rectangular sprite. The vertices may be ordered differently depending on the engine (LibGDX tends to use lower-left origin), but the basic idea looks like this:

![Verts](images/5dOga.png)

A single sprite has 2 triangles -- or 6 vertices. Each *vertex* has 8 attributes `(X, Y, S, T, R, G, B, A)` which together make up `Position`, `TexCoord` and `Color`. This means that with every sprite, we are pushing 48 floats to the stack! A more optimized sprite batcher might pack the RGBA into a single float, or may forgo vertex colors altogether.

## Now where?

Creating your own sprite batcher is not easy, and requires understanding of shaders, vertex buffers, and basic matrix math. Before diving into these advanced topics, I'd recommend getting comfortable with the SpriteBatcher provided for you by [lwjgl-basics](https://github.com/mattdesl/lwjgl-basics). Alternatively, you can use LibGDX as the implementation is very similar. You should also [get comfortable with GLSL](Shaders) before attempting your own sprite batcher.

If you are still keen to learn about how it all works under the hood, see the [ShaderProgram](ShaderProgram-Utility) and [SpriteBatcher](SpriteBatch) articles.