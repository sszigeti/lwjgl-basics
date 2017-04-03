"Lerp Blur" is a name I've given to a technique to simulate a variable blur in real-time. It's suitable for Android, iOS and other fill-rate limited devices that can't rely on multiple render passes and FBOs. 

The basic idea of the "Lerp Blur" is to, in software, create a series of images of increasing blur strengths, and use some form of interpolation between two varying strengths in order to simulate a real-time adjustable blur. See the below image for reference:  
![8x](images/JL3yQ.png)

The technique becomes more interesting (and more efficient) when we take advantage of mipmapping and trilinear filtering.

## Mipmapping

An old-school trick for cheap blurs is to down-sample your image with high quality interpolation (such as those employed by most drivers for mip-mapping), and then up-scale the image with linear filtering. 

![Crap](images/e7zb4.png)

Downscaled to 64x64, upscaled to 256x256. Looks pretty crappy. Now, let's do the above, but after downsampling to 64x64, we'll apply a nice quality gaussian blur (in software) to the downsized image. Rendered at 256x256:

![Nice](images/ZOPd1.png)

That looks better. Now, if we apply a gaussian blur to each mipmap level, we can use this to simulate variable blur strengths. Since each mipmap level is smaller than the last, each successive mipmap level will lead to a greater blur effect when scaled up. This means we need to build our mipmaps manually, in software:

```java
for each mipmap level:
    //... downsample image by half ...
    pixels = downsample(pixels, width, height);

    //... apply blur to downsampled image ...
    blurred = blur(pixels);    
    
    //... upload blurred pixels to the current mipmap level ...
    glTexImage2D(GL_TEXTURE_2D, mipmapLevel, ...)

    mipmapLevel++;
    width = width/2;
    height = height/2;
```

Our texture will use `GL_LINEAR_MIPMAP_LINEAR` as the filter, and `GL_CLAMP_TO_EDGE` for wrap mode.

Now, when rendering, we need to tell GL which mipmap level to sample from, based on how strong we want our blur to appear. We can do this with the optional `bias` parameter for `texture2D`, in order to influence which mipmap level the driver picks from. 

```glsl
...

//bias to influence LOD picking; e.g. "blur strength"
uniform float bias;

void main() {
	//sample from the texture using bias to influence LOD
	vec4 texColor = texture2D(u_texture, vTexCoord, bias);
	gl_FragColor = texColor * vColor;
}
```

We can also achieve the same on GL 1.0 devices with `GL_TEXTURE_LOD_BIAS`, `GL_TEXTURE_MIN_LOD` and `GL_TEXTURE_MAX_LOD`.

The result is that we can "fake" a real-time blur without any extra draw passes or FBOs. The blur is by no means accurate, but on small resolutions it looks pretty good.

![MipmapBlur](images/FAROj.gif)

<sup>(Shown in grayscale for better GIF quality)</sup>

The downside, of course, is that it's not truly real-time, and has to be blurred in software while loading textures. It also increases texture memory by 33%, and makes regular mipmapping moot. Further, the `bias` parameter is not thoroughly tested, and may perform strangely on certain devices. Nevertheless, maybe it will prove useful for certain effects, such as adding depth of field in a top-down 2D space shooter.

You can see a full implementation of the above technique, as well as another solution that doesn't rely on `bias` parameter, in the following article:  
[OpenGL ES Blurs](OpenGL-ES-Blurs)