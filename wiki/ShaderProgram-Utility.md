This page will cover the steps required to create your own re-usable ShaderProgram utility class in LWJGL. Alternatively, you can skip this step and use the more advanced ShaderProgram utility already included in lwjgl-basics: [see here](https://github.com/mattdesl/lwjgl-basics/blob/master/src/mdesl/graphics/glutils/ShaderProgram.java).

## Set-Up

For our purposes, we will only use one vertex and one fragment shader to create our shader programs. Since we plan on targeting GL 2.1, we will also need to specify the attribute locations manually. If we were targeting newer versions of OpenGL (i.e. GLSL 330+), then we could specify the attribute locations with [type qualifiers](http://www.opengl.org/wiki/Type_Qualifier_%28GLSL%29%23Vertex_shader_attribute_index) instead. The basic steps to creating a shader program look like this:

1. Compile the vertex shader source into a shader object.
2. Compile the fragment shader source into a shader object.
3. Create a program ID with `glCreateProgram`.
4. Attach the vertex and shader objects to our program with `glAttachShader`. 
5. If we are targeting 2.1, here is where we would bind any attribute locations manually. For example, we would bind the Position attribute to index 0. For this we use `glBindAttribLocation`. If we are targeting newer versions of GLSL, we can skip this step.
6. We then link the program with `glLinkProgram`.
7. If the program succeeded in compiling, we can now detach and delete the vertex and fragment shader objects as they are no longer needed -- using `glDetachShader` and `glDeleteShader`, respectively. These are only flags for OpenGL, and the objects will be deleted when they are no longer associated with any rendering states.

You can see the entire process for that here:
```java
public ShaderProgram(String vertexShader, String fragmentShader, Map<Integer, String> attributes) throws LWJGLException {
	//compile the String source
	vertex = compileShader(vertexShader, GL_VERTEX_SHADER);
	fragment = compileShader(fragmentShader, GL_FRAGMENT_SHADER);
	
	//create the program
	program = glCreateProgram();
	
	//attach the shaders
	glAttachShader(program, vertex);
	glAttachShader(program, fragment);

	//bind the attrib locations for GLSL 120
	if (attributes != null)
		for (Entry<Integer, String> e : attributes.entrySet())
			glBindAttribLocation(program, e.getKey(), e.getValue());

	//link our program
	glLinkProgram(program);

	//grab our info log
	String infoLog = glGetProgramInfoLog(program, glGetProgrami(program, GL_INFO_LOG_LENGTH));
	
	//if some log exists, append it 
	if (infoLog!=null && infoLog.trim().length()!=0)
		log += infoLog;
	
	//if the link failed, throw some sort of exception
	if (glGetProgrami(program, GL_LINK_STATUS) == GL_FALSE)
		throw new LWJGLException(
				"Failure in linking program. Error log:\n" + infoLog);
	
	//detach and delete the shaders which are no longer needed
	glDetachShader(program, vertex);
	glDetachShader(program, fragment);
	glDeleteShader(vertex);
	glDeleteShader(fragment);
}

protected int compileShader(String source, int type) throws LWJGLException {
	//create a shader object
	int shader = glCreateShader(type);
	//pass the source string
	glShaderSource(shader, source);
	//compile the source
	glCompileShader(shader);

	//if info/warnings are found, append it to our shader log
	String infoLog = glGetShaderInfoLog(shader,
			glGetShaderi(shader, GL_INFO_LOG_LENGTH));
	if (infoLog!=null && infoLog.trim().length()!=0)
		log += getName(type) +": "+infoLog + "\n";
	
	//if the compiling was unsuccessful, throw an exception
	if (glGetShaderi(shader, GL_COMPILE_STATUS) == GL_FALSE)
		throw new LWJGLException("Failure in compiling " + getName(type)
				+ ". Error log:\n" + infoLog);

	return shader;
}
```


## Using the Program

In OpenGL, we can only have a single shader program in use at a time. We call `glUseProgram(program)` to specify the active program. Back in fixed-function days, we would specify `glUseProgram(0)` to use the "default" shader. However, since we are trying to work with the programmable pipeline, we should no longer concern ourselves with the default shader, since there is no such thing in modern GL. In fact, it may cause errors if we try rendering with the default shader in GL 3.1+ core profile. So our methods to the end-user look like this:
```java
/**
 * Make this shader the active program.
 */
public void use() {
	glUseProgram(program);
}

/**
 * Destroy this shader program.
 */
public void destroy() {
	//a flag for GL -- the program will not actually be deleted until it's no longer in use
	glDeleteProgram(program);
}

/**
 * Gets the location of the specified uniform name.
 * @param str the name of the uniform
 * @return the location of the uniform in this program
 */
public int getUniformLocation(String str) {
	return glGetUniformLocation(program, str);
}
```


## Setting Uniform Values

As discussed in the earlier series, we use `glUniform` to pass uniform data to our shaders. A complete ShaderProgram utility may include numerous utilities for getting and setting uniforms (see [here](https://github.com/mattdesl/lwjgl-basics/blob/master/src/mdesl/graphics/glutils/ShaderProgram.java)). Our simple example will deal with the bare minimum: matrices and integer uniforms (for sampler2D).

```java
/**
 * Sets the uniform data at the specified location (the uniform type may be int, bool or sampler2D). 
 * @param loc the location of the int/bool/sampler2D uniform 
 * @param i the value to set
 */
public void setUniformi(int loc, int i) {
	if (loc==-1) return;
	glUniform1i(loc, i);
}

/**
 * Sends a 4x4 matrix to the shader program.
 * @param loc the location of the mat4 uniform
 * @param transposed whether the matrix should be transposed
 * @param mat the matrix to send
 */
public void setUniformMatrix(int loc, boolean transposed, Matrix4f mat) {
	if (loc==-1) return;
	if (buf16Pool == null)
		buf16Pool = BufferUtils.createFloatBuffer(16);
	buf16Pool.clear();
	mat.store(buf16Pool);
	buf16Pool.flip();
	glUniformMatrix4(loc, transposed, buf16Pool);
}
```

**Note:** Our `setUniform` methods assume the program is already in use.


## Full Java Source
```java
public class ShaderProgram {

	protected static FloatBuffer buf16Pool;
	
	/**
	 * Makes the "default shader" (0) the active program. In GL 3.1+ core profile,
	 * you may run into glErrors if you try rendering with the default shader. 
	 */
	public static void unbind() {
		glUseProgram(0);
	}

	public final int program;
	public final int vertex;
	public final int fragment;
	protected String log;

	public ShaderProgram(String vertexSource, String fragmentSource) throws LWJGLException {
		this(vertexSource, fragmentSource, null);
	}

	/**
	 * Creates a new shader from vertex and fragment source, and with the given 
	 * map of <Integer, String> attrib locations
	 * @param vertexShader the vertex shader source string
	 * @param fragmentShader the fragment shader source string
	 * @param attributes a map of attrib locations for GLSL 120
	 * @throws LWJGLException if the program could not be compiled and linked
	 */
	public ShaderProgram(String vertexShader, String fragmentShader, Map<Integer, String> attributes) throws LWJGLException {
		//compile the String source
		vertex = compileShader(vertexShader, GL_VERTEX_SHADER);
		fragment = compileShader(fragmentShader, GL_FRAGMENT_SHADER);
		
		//create the program
		program = glCreateProgram();
		
		//attach the shaders
		glAttachShader(program, vertex);
		glAttachShader(program, fragment);

		//bind the attrib locations for GLSL 120
		if (attributes != null)
			for (Entry<Integer, String> e : attributes.entrySet())
				glBindAttribLocation(program, e.getKey(), e.getValue());

		//link our program
		glLinkProgram(program);

		//grab our info log
		String infoLog = glGetProgramInfoLog(program, glGetProgrami(program, GL_INFO_LOG_LENGTH));
		
		//if some log exists, append it 
		if (infoLog!=null && infoLog.trim().length()!=0)
			log += infoLog;
		
		//if the link failed, throw some sort of exception
		if (glGetProgrami(program, GL_LINK_STATUS) == GL_FALSE)
			throw new LWJGLException(
					"Failure in linking program. Error log:\n" + infoLog);
		
		//detach and delete the shaders which are no longer needed
		glDetachShader(program, vertex);
		glDetachShader(program, fragment);
		glDeleteShader(vertex);
		glDeleteShader(fragment);
	}

	/** Compile the shader source as the given type and return the shader object ID. */
	protected int compileShader(String source, int type) throws LWJGLException {
		//create a shader object
		int shader = glCreateShader(type);
		//pass the source string
		glShaderSource(shader, source);
		//compile the source
		glCompileShader(shader);

		//if info/warnings are found, append it to our shader log
		String infoLog = glGetShaderInfoLog(shader,
				glGetShaderi(shader, GL_INFO_LOG_LENGTH));
		if (infoLog!=null && infoLog.trim().length()!=0)
			log += getName(type) +": "+infoLog + "\n";
		
		//if the compiling was unsuccessful, throw an exception
		if (glGetShaderi(shader, GL_COMPILE_STATUS) == GL_FALSE)
			throw new LWJGLException("Failure in compiling " + getName(type)
					+ ". Error log:\n" + infoLog);

		return shader;
	}

	protected String getName(int shaderType) {
		if (shaderType == GL_VERTEX_SHADER)
			return "GL_VERTEX_SHADER";
		if (shaderType == GL_FRAGMENT_SHADER)
			return "GL_FRAGMENT_SHADER";
		else
			return "shader";
	}

	/**
	 * Make this shader the active program.
	 */
	public void use() {
		glUseProgram(program);
	}

	/**
	 * Destroy this shader program.
	 */
	public void destroy() {
		glDeleteProgram(program);
	}

	/**
	 * Gets the location of the specified uniform name.
	 * @param str the name of the uniform
	 * @return the location of the uniform in this program
	 */
	public int getUniformLocation(String str) {
		return glGetUniformLocation(program, str);
	}
	
	/* ------ UNIFORM SETTERS/GETTERS ------ */
	
	/**
	 * Sets the uniform data at the specified location (the uniform type may be int, bool or sampler2D). 
	 * @param loc the location of the int/bool/sampler2D uniform 
	 * @param i the value to set
	 */
	public void setUniformi(int loc, int i) {
		if (loc==-1) return;
		glUniform1i(loc, i);
	}

	/**
	 * Sends a 4x4 matrix to the shader program.
	 * @param loc the location of the mat4 uniform
	 * @param transposed whether the matrix should be transposed
	 * @param mat the matrix to send
	 */
	public void setUniformMatrix(int loc, boolean transposed, Matrix4f mat) {
		if (loc==-1) return;
		if (buf16Pool == null)
			buf16Pool = BufferUtils.createFloatBuffer(16);
		buf16Pool.clear();
		mat.store(buf16Pool);
		buf16Pool.flip();
		glUniformMatrix4(loc, transposed, buf16Pool);
	}
}
```