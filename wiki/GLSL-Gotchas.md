Here are some gotchas to be aware of when working with GLSL on various platforms.

## Mac OSX

- Array declaration is broken on Snow Leopard [(1)](http://openradar.appspot.com/6121615)

## Android, iOS, WebGL

- Specify precision where possible. Low precision is useful for colors (0.0 - 1.0). More info [here](http://updates.html5rocks.com/2011/12/Use-mediump-precision-in-WebGL-when-possible).
- Be mindful of `step()` as it may create branching (although it really shouldn't). Benchmark with `smoothstep()` to see if performance improves.
- 'For' loops may cause problems on certain Android devices [(1)](http://badlogicgames.com/forum/viewtopic.php?f=15&t=7801&p=35649&hilit=tegra#p35649)
- On WebGL, you don't need `#ifdef GL_ES` as it will always return true
- Many more optimizations listed [here](http://docs.nvidia.com/tegra/data/Optimize_OpenGL_ES_2_0_Performance_for_Tegra.html)