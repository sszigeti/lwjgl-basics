Here is how to modify the brightness/contrast of sprites and images rendered in LibGDX. 

## GL11 Brightness

In OpenGL 1.1 you simply change the texture environment mode. The default is `GL_MODULATE` -- i.e. multiply vertex color by texel color. This allows us to easily darken an image, for example multiplying it by `0.5`. To brighten an image, we would use `GL_ADD` -- for e.g. vertex color `(0, 0, 0)` will do nothing, and `(1, 1, 1)` will turn the image pure white. (GL clamps the final value between 0.0 and 1.0)

It would look like this in code:
```java
//if we are brightening, use GL_ADD. if we are darkening, use GL_MODULATE
Gdx.gl11.glTexEnvi(GL11.GL_TEXTURE_ENV, GL11.GL_TEXTURE_ENV_MODE, GL11.GL_ADD);

batch.begin();
//0.0 => do nothing, 1.0 => full brightness
batch.setColor(brighten, brighten, brighten, 0f);
batch.draw(...);
batch.draw(...);
batch.end();

//we should reset the tex env to GL_MODULATE
Gdx.gl11.glTexEnvi(GL11.GL_TEXTURE_ENV, GL11.GL_TEXTURE_ENV_MODE, GL11.GL_MODULATE);
```

## GL20 Brightness & Contrast

If we are using the programmable pipeline, the above solution would not be possible. You could use multiple draw calls with a particular blend mode, but that may get expensive. This is where shaders come into use.

ShaderBatch.java  
https://gist.github.com/4255544

This implementation allows you to change brightness and contrast. You might use it like so:
```java
... create ...
		shaderBatch = new ShaderBatch(100); //tweak your size to minimize memory waste
		if (!shaderBatch.isCompiled) {
			System.err.println(shaderBatch.log); //due to GL11 or an error compiling shader
			//if we try using it now, it will behave just like a regular sprite batch
		}

... render ...
		shaderBatch.brightness = 0.5f; // 0.0 -> no change
		shaderBatch.contrast = 1.5f; // 1.0 -> no change
		shaderBatch.begin();
		shaderBatch.draw(...);
		shaderBatch.end();
```

The problem with this is that you need to flush the batch (begin/end) every time you want to change the brightness or contrast. If you are doing this per-sprite, then it can become costly and defeats the purpose of a batch. It also means you are using two SpriteBatches in your application, which is generally a heavy object. A more involved solution might be to pass the brightness/contrast as a custom attribute to your shader, and create your own sprite batcher of sorts using LibGDX's Mesh utility. Ultimately it really depends on your game and how you need this feature to be implemented. Also be sure to check out the [Shader Tutorial Series](Shaders) as it will help you understand what's going on a bit better.

If you want more accurate/advanced brightness and contrast algorithms, see here:  
http://www.dfstudios.co.uk/articles/image-processing-algorithms-part-5/#comment-20632  
http://www.kweii.com/site/color_theory/2007_LV/BrightnessCalculation.pdf