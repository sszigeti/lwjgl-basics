##### [start](https://github.com/mattdesl/lwjgl-basics/wiki) » [Shaders](Shaders) » Lesson 6: Normal Mapping

***

This series relies on the minimal [lwjgl-basics](https://github.com/mattdesl/lwjgl-basics) API for shader and rendering utilities. The code has also been [Ported to LibGDX](#Ports). The concepts should be universal enough that they could be applied to [Love2D](https://love2d.org/), [GLSL Sandbox](http://glsl.heroku.com/), iOS, or any other platforms that support GLSL. 

***

## Intro

This article will focus on 3D lighting and normal mapping techniques and how we can apply them to 2D games. To demonstrate, see the following. On the left is the texture, and on the right is the illumination applied in real-time.    
![Rock](images/e4FtQNt.png)
![Lit](images/WHI3uYo.gif)

Once you understand the concept of illumination, it should be fairly straight-forward to apply it to any setting. Here is an example of normal mapping in a Java4K demo, i.e. rendered in software:    
![Pixels](images/S6ElW.gif)

The effect is the same shown in [this popular YouTube video](http://youtu.be/vtYvNEmmHXE) and [this Love2D demo](https://love2d.org/forums/viewtopic.php?f=5&t=11076). You can also see the effect in action [here](http://www.java-gaming.org/topics/glsl-using-normal-maps-to-illuminate-a-2d-texture-libgdx/27516/view.html), which includes an executable demo.

## Contents

- [Intro to Vectors & Normals](#VectorsNormals)
- [Encoding & Decoding Normals](#EncDecNormals)
- [Lambertian Illumination Model](#IlluminationModel)
- [Java Code Example](#JavaCode)
  - [Fragment Shader](#FragmentShader)
  - [GLSL Breakdown](#Breakdown)
- [Gotchas](#Gotchas)
- [Multiple Lights](#MultipleLights)
- [Generating Normal Maps](#GeneratingNormals)
  - [Blender Tool](#BlenderTool)
- [Further Reading](#FurtherReading)
- [Appendix: Pixel Art](#Appendix)
- [Other APIs](#Ports)

<a name="VectorsNormals" />
## Intro to Vectors & Normals

As we've discussed in past lessons, a GLSL "vector" is a float container that typically holds values such as position; `(x, y, z)`. In mathematics, vectors mean quite a bit more, and are used to denote length (i.e. magnitude) and direction. If you're new to vectors and want to learn a bit more about them, check out some of these links:

- [Basic 3D Math](http://www.matrix44.net/cms/notes/opengl-3d-graphics/basic-3d-math-vectors)
- [Vector Math for Graphics](http://programmedlessons.org/VectorLessons/index.html)
- [Mathematics of Vectors Applied to Graphics](http://3dgep.com/?p=359)

To calculate lighting, we need to use the "normal" vectors of a mesh. A surface normal is a vector perpendicular to the tangent plane. In simpler terms, it's a vector that is perpendicular to the mesh at a given vertex. Below we see a mesh with the normal for each vertex.  
![Mesh1](images/QnfZ4.png)

Each vector points outward, following the curvature of the mesh. Here is another example, this time a simplified 2D side view:  
![LightLow](images/MLTGx.png)

"Normal Mapping" is a game programming trick that allows us to render the same number of polygons (i.e. a low-res mesh), but use the normals of our high-res mesh when calculating the lighting. This gives us a much greater sense of depth, realism and smoothness:  
![Light](images/5EH9m.png)

<sub>(Images from [this great blog post](http://acko.net/blog/making-worlds-3-thats-no-moon/))</sub>

The normals of the high poly mesh or "sculpt" are encoded into a texture (AKA normal map), which we sample from in our fragment shader while rendering the low poly mesh. The results speak for themselves:  
![RealTime](images/17dVa.png)

<a name="EncDecNormals" />
## Encoding & Decoding Normals

Our surface normals are unit vectors typically in the range -1.0 to 1.0. We can store the normal vector `(x, y, z)` in a RGB texture by converting the normal to the range 0.0 to 1.0. Here is some pseudo-code:
```glsl
Color.rgb = Normal.xyz / 2.0 + 0.5;
```

For example, a normal of `(-1, 0, 1)` would be encoded as RGB `(0, 0.5, 1)`. The x-axis (left/right) is stored in the red channel, the y-axis (up/down) stored in the green channel, and the z-axis (forward/backward) is stored in the blue channel. The resulting "normal map" looks ilke this:  
![NormalMap](images/pgfKp.png)

Typically, we use a program to [generate our normal map](#GeneratingNormals) rather than painting them by hand.

To understand the normal map, it's clearer to look at each channel individually:  
![Channels](images/ppXbS.png)

Looking at, say, the green channel, we see that the brighter parts (values closer to `1.0`) define areas where the normal would point upward, whereas darker areas (values closer to `0.0`) define areas where the normal would point downward. Most normal maps will have a bluish tint because the Z axis (blue channel) is generally pointing toward us (i.e. value of `1.0`). 

In our game's fragment shader, we can "decode" the normals by doing the reverse of what we did earlier, expanding the color value to the range -1.0 to 1.0:
```glsl
//sample the normal map
NormalMap = texture2D(NormalMapTex, TexCoord);

//convert to range -1.0 to 1.0
Normal.xyz = NormalMap.rgb * 2.0 - 1.0;
```

*Note:* Keep in mind that different engines and programs will use different coordinate systems, and the green channel may need to be inverted.

<a name="IlluminationModel" />
# Lambertian Illumination Model

In computer graphics, we have a number of algorithms that can be combined to create different shading results for a 3D object. In this article we will focus on Lambert shading, without any specular (i.e. "gloss" or "shininess"). Other techniques, like Phong, Cook-Torrance, and Oren–Nayar can be used to produce different visual results (rough surfaces, shiny surfaces, etc).

Our entire illumination model looks like this:

```
N = normalize(Normal.xyz)
L = normalize(LightDir.xyz)

Diffuse = LightColor * max(dot(N, L), 0.0)

Ambient = AmbientColor * AmbientIntensity

Attenuation = 1.0 / (ConstantAtt + (LinearAtt * Distance) + (QuadraticAtt * Distance * Distance)) 

Intensity = Ambient + Diffuse * Attenuation

FinalColor = DiffuseColor.rgb * Intensity.rgb
```

In truth, you don't need to understand why this works mathematically, but if you are interested you can read more about "N dot L" shading [here](http://www.lighthouse3d.com/tutorials/glsl-core-tutorial/directional-lights/) and [here](http://en.wikipedia.org/wiki/Lambertian_reflectance).

Some key terms:

- **Normal:** This is the normal XYZ that we decoded from out NormalMap texture.
- **LightDir:** This is the vector from the surface to the light position, which we will explain shortly.
- **Diffuse Color:** This is the RGB of our texture, unlit.
- **Diffuse:** The light color multiplied by Lambertian reflection. This is the "meat" of our lighting equation.
- **Ambient:** The color and intensity when in shadow. For example, an outdoor scene may have a higher ambient intensity than a dimly lit indoor scene. 
- **Attenuation:** This is the "distance falloff" of the light; i.e. the loss of intensity/brightness as we move further from the point light. There are a number of ways of calculating attenuation -- for our purposes we will use ["Constant-Linear-Quadratic" attenuation](https://developer.valvesoftware.com/wiki/Constant-Linear-Quadratic_Falloff). The attenuation is calculated with three "coefficients" which we can change to affect how the light falloff looks.
- **Intensity:** This is the intensity of our shading algorithm -- closer to 1.0 means "lit" while closer to 0.0 means "unlit."

The following image will help you visualize our illumination model:

![Illu](images/bSbNxRh.png)

As you can see, it's rather "modular" in the sense that we can take away parts of it that we might not need, like attenuation or light colors. 

Now let's try to apply this to model GLSL. Note that we will only be working with 2D, and there are some [extra considerations in 3D](http://www.ozone3d.net/tutorials/bump_mapping_p3.php#tangent_space) that are not covered by this tutorial. We will break the model down into separate parts, each one building on the next.

<a name="JavaCode" />
## Java Code Example

You can see the Java code example [here](https://github.com/mattdesl/lwjgl-basics/blob/master/test/mdesl/test/shadertut/ShaderLesson6.java). It's relatively straight-forward, and doesn't introduce much that hasn't been discussed in earlier lessons. We'll use the following two textures:

![Rock](images/e4FtQNt.png)
![RockN](images/cjFUm7X.png)  

Our example adjusts the `LightPos.xy` based on the mouse position (normalized to resolution), and `LightPos.z` (depth) based on the mouse wheel (click to reset light Z). With certain coordinate systems, like LibGDX, you may need to flip the Y value. 

Note that our example uses the following constants, which you can play with to get a different look:
```java
public static final float DEFAULT_LIGHT_Z = 0.075f;
...
//Light RGB and intensity (alpha)
public static final Vector4f LIGHT_COLOR = new Vector4f(1f, 0.8f, 0.6f, 1f);

//Ambient RGB and intensity (alpha)
public static final Vector4f AMBIENT_COLOR = new Vector4f(0.6f, 0.6f, 1f, 0.2f);

//Attenuation coefficients for light falloff
public static final Vector3f FALLOFF = new Vector3f(.4f, 3f, 20f);
```

Below is our rendering code. Like in [Lesson 4](ShaderLesson4), we will use multiple texture units when rendering.
```java
...

//update light position, normalized to screen resolution
float x = Mouse.getX() / (float)Display.getWidth();
float y = Mouse.getY() / (float)Display.getHeight();
LIGHT_POS.x = x;
LIGHT_POS.y = y;

//send a Vector4f to GLSL
shader.setUniformf("LightPos", LIGHT_POS);

//bind normal map to texture unit 1
glActiveTexture(GL_TEXTURE1);
rockNormals.bind();

//bind diffuse color to texture unit 0
glActiveTexture(GL_TEXTURE0);
rock.bind();

//draw the texture unit 0 with our shader effect applied
batch.draw(rock, 50, 50);
```

The resulting "shaded" texture:  
![Shaded](images/CrkJznv.png)

Here it is again, using a lower Z value for the light:  
![Z](images/pZ7gajb.png)

<a name="FragmentShader" />
### Fragment Shader

Here is our full fragment shader, which we will break down in the next section:

```glsl
//attributes from vertex shader
varying vec4 vColor;
varying vec2 vTexCoord;

//our texture samplers
uniform sampler2D u_texture;   //diffuse map
uniform sampler2D u_normals;   //normal map

//values used for shading algorithm...
uniform vec2 Resolution;      //resolution of screen
uniform vec3 LightPos;        //light position, normalized
uniform vec4 LightColor;      //light RGBA -- alpha is intensity
uniform vec4 AmbientColor;    //ambient RGBA -- alpha is intensity 
uniform vec3 Falloff;         //attenuation coefficients

void main() {
	//RGBA of our diffuse color
	vec4 DiffuseColor = texture2D(u_texture, vTexCoord);
	
	//RGB of our normal map
	vec3 NormalMap = texture2D(u_normals, vTexCoord).rgb;
	
	//The delta position of light
	vec3 LightDir = vec3(LightPos.xy - (gl_FragCoord.xy / Resolution.xy), LightPos.z);
	
	//Correct for aspect ratio
	LightDir.x *= Resolution.x / Resolution.y;
	
	//Determine distance (used for attenuation) BEFORE we normalize our LightDir
	float D = length(LightDir);
	
	//normalize our vectors
	vec3 N = normalize(NormalMap * 2.0 - 1.0);
	vec3 L = normalize(LightDir);
	
	//Pre-multiply light color with intensity
	//Then perform "N dot L" to determine our diffuse term
	vec3 Diffuse = (LightColor.rgb * LightColor.a) * max(dot(N, L), 0.0);

	//pre-multiply ambient color with intensity
	vec3 Ambient = AmbientColor.rgb * AmbientColor.a;
	
	//calculate attenuation
	float Attenuation = 1.0 / ( Falloff.x + (Falloff.y*D) + (Falloff.z*D*D) );
	
	//the calculation which brings it all together
	vec3 Intensity = Ambient + Diffuse * Attenuation;
	vec3 FinalColor = DiffuseColor.rgb * Intensity;
	gl_FragColor = vColor * vec4(FinalColor, DiffuseColor.a);
}
```

<a name="Breakdown" />
### GLSL Breakdown 

Now, to break it down. First, we sample from our two textures:

```glsl
//RGBA of our diffuse color
vec4 DiffuseColor = texture2D(u_texture, vTexCoord);

//RGB of our normal map
vec3 NormalMap = texture2D(u_normals, vTexCoord).rgb;
```

Next, we need to determine the light vector from the current fragment, and correct it for the aspect ratio. Then we determine the magnitude (length) of our `LightDir` vector before we normalize it:
```glsl
//Delta pos
vec3 LightDir = vec3(LightPos.xy - (gl_FragCoord.xy / Resolution.xy), LightPos.z);

//Correct for aspect ratio
LightDir.x *= Resolution.x / Resolution.y;

//determine magnitude
float D = length(LightDir);
```

As in our illumination model, we need to decode the `Normal.xyz` from our `NormalMap.rgb`, and then normalize our vectors:
```glsl
vec3 N = normalize(NormalMap * 2.0 - 1.0);
vec3 L = normalize(LightDir);
```

The next step is to calculate the `Diffuse` term. For this, we need to use `LightColor`. In our case, we will multiply the light color (RGB) by intensity (alpha): `LightColor.rgb * LightColor.a`. So, together it looks like this:
```glsl
//Pre-multiply light color with intensity
//Then perform "N dot L" to determine our diffuse term
vec3 Diffuse = (LightColor.rgb * LightColor.a) * max(dot(N, L), 0.0);
```

Next, we pre-multiply our ambient color with intensity:
```glsl
vec3 Ambient = AmbientColor.rgb * AmbientColor.a;
```

The next step is to use our `LightDir` magnitude (calculated earlier) to determine the `Attenuation`. The `Falloff` uniform defines our Constant, Linear, and Quadratic attenuation coefficients.
```glsl
float Attenuation = 1.0 / ( Falloff.x + (Falloff.y*D) + (Falloff.z*D*D) );
```

Next, we calculate the `Intensity` and `FinalColor`, and pass it to `gl_FragCoord`. Note that we keep the alpha of the `DiffuseColor` in tact.

```glsl
vec3 Intensity = Ambient + Diffuse * Attenuation;
vec3 FinalColor = DiffuseColor.rgb * Intensity;
gl_FragColor = vColor * vec4(FinalColor, DiffuseColor.a);
```

<a name="Gotchas" />
## Gotchas

- The `LightDir` and attenuation in our implementation depends on the resolution. This means that changing the resolution will affect the falloff of our light. Depending on your game, a different implementation may be required that is resolution-independent.
- A common problem has to do with differences between your game's Y coordinate system and that employed by your normal-map generation program (such as CrazyBump). Some programs will let you export with a flipped Y value. The following image shows the problem:  
![FlipY](images/u3vDDfP.png)

<a name="MultipleLights" />
## Multiple Lights

To achieve multiple lights, we simply need to adjust our algorithm like so:
```glsl
vec3 Sum = vec3(0.0);
for (... each light ...) {
    ... calculate light using our illumination model ...
    Sum += FinalColor;
}
gl_FragColor = vec4(Sum, DiffuseColor.a);
```

![Multiple](images/xZeLLSR.png)

Note this introduces more branching to your shader, which may degrade performance. 

This is sometimes known as "N lighting" since our system only supports a fixed *N* number of lights. If you plan to include a lot of lights, you may want to investigate multiple draw calls (i.e. additive blending), or [deferred lighting](http://en.wikipedia.org/wiki/Deferred_shading). 

At a certain point you may ask yourself: "Why don't I just make a 3D game?" This is a valid question and may lead to better performance and less development time than trying to apply these concepts to 2D sprites.

<a name="GeneratingNormals" />
## Generating Normal Maps

There are a number of ways of generating a normal map from an image. Common applications and filters for converting 2D images to normal maps include:

- [SpriteLamp](http://snakehillgames.com/spritelamp/) - specifically aimed at 2D normal-map art
- [SMAK! - Super Model Army Knife](http://getsmak.com/)
- [CrazyBump](http://www.crazybump.com/)
- [NVIDIA Texture Tools for Photoshop](https://developer.nvidia.com/nvidia-texture-tools-adobe-photoshop)
- [gimp-normalmap](http://code.google.com/p/gimp-normalmap/)
- [SSBump Generator](http://ssbump-generator.yolasite.com/)
- [njob](http://charles.hollemeersch.net/njob)
- [ShaderMap](http://shadermap.com/home/)

Note that many of these applications will produce aliasing and inaccuracies, read [this article](http://www.katsbits.com/tutorials/textures/how-not-to-make-normal-maps-from-photos-or-images.php) for further details.

You can also use 3D modeling software like [Blender](http://www.blender.org/) or [ZBrush](http://www.pixologic.com/) to sculpt high-quality normal maps. 

<a name="BlenderTool" />
### Blender Tool

One idea for a workflow would be to produce a low-poly and very rough 3D object of your art asset. Then you can use [this Blender normal map template](https://github.com/mattdesl/lwjgl-basics/tree/master/tools/blender-normals) to render your object to a 2D tangent space normal map. Then, you could open the normal map in Photoshop and begin working on the diffuse color map.

Here's what the Blender template looks like:  
![Image](images/dFRsM.png)

<a name="FurtherReading" />
## Further Reading 

Here are some useful links that go into more detail regarding normal mapping for 3D games:  

- [UpVector - Intro to Shaders & Light](http://www.upvector.com/?section=Tutorials&subsection=Intro%20to%20Shaders)
- [Bump Mapping Using CG by Søren Dreijer](http://www.blacksmith-studios.dk/projects/downloads/bumpmapping_using_cg.php)
- [Illumination Model Slides](http://nccastaff.bournemouth.ac.uk/jmacey/CGF/slides/IlluminationModels4up.pdf)
- [The Cg Tutorial](http://http.developer.nvidia.com/CgTutorial/cg_tutorial_chapter05.html)
- [oZone Bump Mapping Tutorial](http://www.ozone3d.net/tutorials/bump_mapping.php)
- [Bump Mapping in GLSL - Fabien Sanglard](http://fabiensanglard.net/bumpMapping/index.php)

<a name="Appendix" />
## Appendix: Pixel Art

There are a couple of considerations that I had to take into account when creating my WebGL [normal map pixel art](http://mattdesl.github.io/kami-demos/release/normals-pixel.html) demo. You can see the source and details [here](https://github.com/mattdesl/kami-demos/tree/master/src/normals-pixel).

In this demo, I wanted the falloff the be visible as a stylistic element. The typical approach leads to a very smooth falloff, which clashes with the blocky pixel art style. Instead, I used "cel shading" for the light, to give it a stepped falloff. This was achieved with simple [toon shading](http://prideout.net/blog/?p=22) through if-else statements in the fragment shader.

The next consideration is that we want the edge pixels of the light to scale along with the pixels of our sprites. One way of achieving this is to draw our scene to an FBO with the illumination shader, and *then* render it with a default shader to the screen at a larger size. This way the illumination affects whole "texels" in our blocky pixel art. 

<a name="Ports" />

## Other APIs

* [LibGDX Port](https://gist.github.com/4653464)
* [JS/WebGL Port](https://github.com/mattdesl/kami-demos/tree/master/src/normals)
* [JS/WebGL Port (Pixel Art)](https://github.com/mattdesl/kami-demos/tree/master/src/normals-pixel)