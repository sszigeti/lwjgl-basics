##### [start](https://github.com/mattdesl/lwjgl-basics/wiki) » Display

This is a short snippet of code demonstrating a typical application life cycle in LWJGL. The code is pretty self-explanatory. You can find other examples on the [LWJGL wiki](http://www.lwjgl.org/wiki/index.php?title=Main_Page).

The source code is listed [at the end of the article](#Source).

### OpenGL Setup

We need to set up a few things in order for OpenGL to work correctly. Note that we are using static imports; this is a Java feature that allows is to omit the class name, and it proves very useful for OpenGL programming. In Eclipse you can import with wildcard `*` for convenience, and then click Ctrl + Shift + O to organize and auto-correct any imports.

Firstly, it's important to set up our OpenGL viewport to match the display size. We will also call this whenever the display is resized:
```java
glViewport(0, 0, Display.getWidth(), Display.getHeight());
```

Next, we can disable depth testing since most 2D games will not require this. A bit of info here: the depth buffer is used in 3D scenes to ensure that distant objects render correctly, and do not overlap with closer objects. 

In 2D games, we determine which sprites overlap others based on their *draw order* (i.e. sprite B is drawn after sprite A, therefore it will appear on top of sprite A). Some advanced 2D games may make use of the depth buffer for hardware-accelerated depth sorting, but we don't need to worry about that for now.

```java
glDisable(GL_DEPTH_TEST);
```

Next, we need to enable blending. This will be explained in more detail in another series.
Without this enabled, transparent sprites may not render as expected.

```java
glEnable(GL_BLEND);
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
```

We also set the "clear color" in our initialization. This is the color which GL will clear the 
screen to. Keep in mind that colors are specified in RGBA floats in the range 0.0 to 1.0, so here we are specifiying transparent black.
```java
glClearColor(0f, 0f, 0f, 0f);
```

Notice that OpenGL is a "static" and "state based" API. Generally speaking, the states we have set above will not change until we call them with a new parameter. So we don't need to call these methods every frame, unless something (like a 3rd party library) is interfering with our GL states.

### Game Loop

The game loop we have here is very basic. At a later point, you can return to it to implement some timing and interpolation,
such as in [this example](http://www.lwjgl.org/wiki/index.php?title=LWJGL_Basics_4_(Timing)). For now, we rely on LWJGL's
`Display.sync` method to cap the frame-rate at 60 frames per second. 

LWJGL uses double-buffering under the hood; we render to the "back buffer,"
then call `Display.update` to flip the buffers and show the result on screen. As you can see,
we clear the screen each frame with the following line:
```java
glClear(GL_COLOR_BUFFER_BIT);
```

This will clear the screen to the color we specified earlier, transparent black.

The rest of the code should be relatively self-explanitory.

<a name="Source" />
### Full Source Code

```java
/**
 * Copyright (c) 2012, Matt DesLauriers All rights reserved.
 *
 *	Redistribution and use in source and binary forms, with or without
 *	modification, are permitted provided that the following conditions are met: 
 *
 *	* Redistributions of source code must retain the above copyright notice, this
 *	  list of conditions and the following disclaimer. 
 *
 *	* Redistributions in binary
 *	  form must reproduce the above copyright notice, this list of conditions and
 *	  the following disclaimer in the documentation and/or other materials provided
 *	  with the distribution. 
 *
 *	* Neither the name of the Matt DesLauriers nor the names
 *	  of his contributors may be used to endorse or promote products derived from
 *	  this software without specific prior written permission.
 *
 *	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 *	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *	ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 *	LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 *	CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 *	SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 *	INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 *	CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *	ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *	POSSIBILITY OF SUCH DAMAGE.
 */
package mdesl.test;

import static org.lwjgl.opengl.GL11.GL_BLEND;
import static org.lwjgl.opengl.GL11.GL_COLOR_BUFFER_BIT;
import static org.lwjgl.opengl.GL11.GL_DEPTH_TEST;
import static org.lwjgl.opengl.GL11.GL_ONE_MINUS_SRC_ALPHA;
import static org.lwjgl.opengl.GL11.GL_SRC_ALPHA;
import static org.lwjgl.opengl.GL11.glBlendFunc;
import static org.lwjgl.opengl.GL11.glClear;
import static org.lwjgl.opengl.GL11.glClearColor;
import static org.lwjgl.opengl.GL11.glDisable;
import static org.lwjgl.opengl.GL11.glEnable;
import static org.lwjgl.opengl.GL11.glViewport;

import org.lwjgl.LWJGLException;
import org.lwjgl.opengl.Display;
import org.lwjgl.opengl.DisplayMode;

/**
 * A bare-bones implementation of a LWJGL application.
 * @author davedes
 */
public class Game {
	
	// Whether to enable VSync in hardware.
	public static final boolean VSYNC = true;
	
	// Width and height of our window
	public static final int WIDTH = 800;
	public static final int HEIGHT = 600;
	
	// Whether to use fullscreen mode
	public static final boolean FULLSCREEN = false;
	
	// Whether our game loop is running
	protected boolean running = false;
	
	public static void main(String[] args) throws LWJGLException {
		new Game().start();
	}
	
	// Start our game
	public void start() throws LWJGLException {
		// Set up our display 
		Display.setTitle("Display example"); //title of our window
		Display.setResizable(true); //whether our window is resizable
		Display.setDisplayMode(new DisplayMode(WIDTH, HEIGHT)); //resolution of our display
		Display.setVSyncEnabled(VSYNC); //whether hardware VSync is enabled
		Display.setFullscreen(FULLSCREEN); //whether fullscreen is enabled

		//create and show our display
		Display.create();
		
		// Create our OpenGL context and initialize any resources
		create();
		
		// Call this before running to set up our initial size
		resize();

		running = true;
		
		// While we're still running and the user hasn't closed the window... 
		while (running && !Display.isCloseRequested()) {
			// If the game was resized, we need to update our projection
			if (Display.wasResized())
				resize();
			
			// Render the game
			render();
			
			// Flip the buffers and sync to 60 FPS
			Display.update();
			Display.sync(60);
		}
		
		// Dispose any resources and destroy our window
		dispose();
		Display.destroy();
	}
	
	// Exit our game loop and close the window
	public void exit() {
		running = false;
	}
	
	// Called to setup our game and context
	protected void create() {
		// 2D games generally won't require depth testing 
		glDisable(GL_DEPTH_TEST);
		
		// Enable blending
		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
		
		// Set clear to transparent black
		glClearColor(0f, 0f, 0f, 0f);
				
		// ... initialize resources here ...
	}
	
	// Called to render our game
	protected void render() {
		// Clear the screen
		glClear(GL_COLOR_BUFFER_BIT);
		
		// ... render our game here ...
	}
	
	// Called to resize our game
	protected void resize() {
		glViewport(0, 0, Display.getWidth(), Display.getHeight());
		// ... update our projection matrices here ...
	}
	
	// Called to destroy our game upon exiting
	protected void dispose() {
		// ... dispose of any textures, etc ...
	}
}
```