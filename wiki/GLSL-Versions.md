# Intro

You can use the `#version` command as the first line of your shader to specify GLSL version:

```glsl
#version 120

void main() {
    gl_FragColor = vec4(1.0);
}
```

GLSL versions are released alongside GL versions. See the following charts to decide which version you would like to target.

### GLSL Versions

<table>
    <tr>
        <td><b>OpenGL Version</b></td>
        <td><b>GLSL Version</b></td>
    </tr>
    <tr>
        <td>2.0</td>
        <td>110</td>
    </tr>
    <tr>
        <td>2.1</td>
        <td>120</td>
    </tr>
    <tr>
        <td>3.0</td>
        <td>130</td>
    </tr>
    <tr>
        <td>3.1</td>
        <td>140</td>
    </tr>
    <tr>
        <td>3.2</td>
        <td>150</td>
    </tr>
    <tr>
        <td>3.3</td>
        <td>330</td>
    </tr>
    <tr>
        <td>4.0</td>
        <td>400</td>
    </tr>
    <tr>
        <td>4.1</td>
        <td>410</td>
    </tr>
    <tr>
        <td>4.2</td>
        <td>420</td>
    </tr>
    <tr>
        <td>4.3</td>
        <td>430</td>
    </tr>
</table>

### GLSL ES Versions (Android, iOS, WebGL)

OpenGL ES has its own Shading Language, and the versioning starts fresh. It is based on OpenGL Shading Language version 1.10.

<table>
    <tr>
        <td><b>OpenGL ES Version</b></td>
        <td><b>GLSL ES Version</b></td>
    </tr>
    <tr>
        <td>2.0</td>
        <td>100</td>
    </tr>
    <tr>
        <td>3.0</td>
        <td>300</td>
    </tr>
</table>

So, for example, if a feature is available in GLSL 120, it probably won't be available in GLSL ES 100 unless the ES compiler specifically allows it.

# Differences at a Glance

Differences between (desktop) GLSL versions.

## Version 100

Vertex shader:
```glsl
uniform mat4 projTrans;

attribute vec2 Position;
attribute vec2 TexCoord;

varying vec2 vTexCoord;

void main() {
	vTexCoord = TexCoord;
	gl_Position = u_projView * vec4(Position, 0.0, 1.0);
}
```

Fragment shader:
```glsl
uniform sampler2D tex0;

varying vec2 vTexCoord;

void main() {
    vec4 color = texture2D(tex0, vTexCoord);
    gl_FragColor = color;
}
```

## Version 330

As of GLSL 130+, `in` and `out` are used instead of `attribute` and `varying`. GLSL 330+ includes other features like layout qualifiers and changes `texture2D` to `texture`.

Vertex shader:
```glsl
#version 330

uniform mat4 projTrans;

layout(location = 0) in vec2 Position;
layout(location = 1) in vec2 TexCoord;

out vec2 vTexCoord;

void main() {
	vTexCoord = TexCoord;
	gl_Position = u_projView * vec4(Position, 0, 1);
}
```

Fragment shader:
```glsl
#version 330
uniform sampler2D tex0;

in vec2 vTexCoord;

//use your own output instead of gl_FragColor 
out vec4 fragColor;

void main() {
    //'texture' instead of 'texture2D'
    fragColor = texture(tex0, vTexCoord);
}
```

# Other Significant Changes

## GLSL 120 Additions

- You can initialize arrays within a shader, like so:
```glsl
float a[5] = float[5](3.4, 4.2, 5.0, 5.2, 1.1);
float b[5] = float[](3.4, 4.2, 5.0, 5.2, 1.1);
```
However, the above is not supported on Mac OSX Snow Leopard, even with GLSL 120. [(1)](http://openradar.appspot.com/6121615) 
- You can initialize uniforms in a shader, and the value will be set at link time:
```glsl
uniform float val = 1.0;
```
- You can use built-ins like `sin()` when setting a `const` value
- Integers are implicitly converted to floats when necessary, for example:
```glsl
float f = 1.0; <-- valid
float g = 1; <-- only supported in GLSL 120
vec2 v = vec2(1, 2.0); <-- only supported in GLSL 120
```
- You can use `f` to define a float: `float f = 2.5f;`

## GLSL 130 Additions

- `int` and `uint` support (and bitwise operations with them)
- `switch` statement support
- New built-ins: `trunc()`, `round()`, `roundEven()`, `isnan()`, `isinf()`, `modf()`
- Fragment output can be user-defined
- Input and output is declared with `in` and `out` syntax instead of `attribute` and `varying`

## GLSL 150 Additions

- `texture()` should now be used instead of `texture2D()`

## GLSL 330 Additions

- Layout qualifiers can declare the location of vertex shader inputs and fragment shader outputs, eg: 
```glsl
layout(location = 2) in vec3 values[4];
```
Formally this was only possible with `ARB_explicit_attrib_location` extension