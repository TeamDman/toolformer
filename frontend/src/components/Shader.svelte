<!-- inspired by https://t.me/strangerintheq -->
<script lang="ts">
	import { browser } from "$app/environment";
	import { onDestroy, onMount } from "svelte";
	function setup(canvas: HTMLCanvasElement) {
		const gl = canvas!.getContext("webgl")!;
		const program = gl.createProgram()!;
		const vertexShaderSource = `
            precision mediump float;

            attribute vec2 position;
            uniform float time;
            void main() {
                gl_Position = vec4(position, 0.0, 1.0);
                float scale = 0.2;
                gl_Position.x = position.x*scale * cos(time) - position.y*scale * sin(time);
                gl_Position.x += 0.5 * sin(time);
                gl_Position.y = position.x*scale * sin(time) + position.y*scale * cos(time);
                gl_Position.y += 0.5 * cos(time);
            }
        `;
		const fragmentShaderSource = `
            precision mediump float;
        
            uniform float time;
            uniform vec2 resolution;

            void main() {
                float u = gl_FragCoord.x / resolution.x;
                float v = gl_FragCoord.y / resolution.y;

                float r = 0.5 + 0.5 * cos(time * 0.5 + u * 10.0);
                float g = 0.5 + 0.5 * sin(time * 0.7 + v * 5.0);
                float b = 0.5 + 0.5 * cos(time * 0.3 + u * v * 20.0);

                gl_FragColor = vec4(r, g, b, 1.0);
            }
        `;

		const vertexShader = gl.createShader(gl.VERTEX_SHADER)!;
		gl.shaderSource(vertexShader, vertexShaderSource);
		gl.compileShader(vertexShader);
		if (!gl.getShaderParameter(vertexShader, gl.COMPILE_STATUS)) {
			console.error("Error compiling vertex shader", gl.getShaderInfoLog(vertexShader));
			return;
		}

		const fragmentShader = gl.createShader(gl.FRAGMENT_SHADER)!;
		gl.shaderSource(fragmentShader, fragmentShaderSource);
		gl.compileShader(fragmentShader);
		if (!gl.getShaderParameter(fragmentShader, gl.COMPILE_STATUS)) {
			console.error("Error compiling fragment shader", gl.getShaderInfoLog(fragmentShader));
			return;
		}

		gl.attachShader(program, vertexShader);
		gl.attachShader(program, fragmentShader);
		gl.linkProgram(program);
		if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
			console.error("Error linking program", gl.getProgramInfoLog(program));
			return;
		}
		gl.useProgram(program);

		const positionAttributeLocation = gl.getAttribLocation(program, "position");
		const timeUniformLocation = gl.getUniformLocation(program, "time");
		const resolutionUniformLocation = gl.getUniformLocation(program, "resolution");

		const positionBuffer = gl.createBuffer();
		gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
		const positions = [0.0, 0.5, -0.5, -0.5, 0.5, -0.5];
		gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);
		gl.enableVertexAttribArray(positionAttributeLocation);
		gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);

		function render(time: number) {
			gl.viewport(0, 0, width, height);
			gl.clearColor(0.0, 0.0, 0.0, 1.0);
			gl.clear(gl.COLOR_BUFFER_BIT);
			gl.uniform1f(timeUniformLocation, time / 300);
			gl.uniform2f(resolutionUniformLocation, width, height);
			gl.drawArrays(gl.TRIANGLES, 0, 3);
			latestReq = requestAnimationFrame(render);
		}
		latestReq = requestAnimationFrame(render);
	}
	let canvas: HTMLCanvasElement;
	let latestReq = -1;

	let width: number;
	let height: number;

	if (browser) {
		onMount(() => {
			setup(canvas);
		});
		onDestroy(() => {
			cancelAnimationFrame(latestReq);
		});
	}
</script>

<svelte:window bind:innerWidth={width} bind:innerHeight={height} />

<canvas {width} {height} bind:this={canvas} />
