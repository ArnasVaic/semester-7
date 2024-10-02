$(function() {
  const canvas = $("#canvas")[0];
  const ctx = canvas.getContext("2d");
  const L = 512;
  const PI = Math.PI;

  const FIGURE_LENGTH = 4;
  const FIGURE_MASK = [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [0, 0, 1, 1],
    [0, 0, 1, 1],
  ];

  console.assert(FIGURE_LENGTH == FIGURE_MASK.length);
  console.assert(
    FIGURE_MASK.map((row) => row.length == FIGURE_LENGTH).reduce((a, b) => a && b)
  );

  const FRACTAL_CONFIG = [
    {
      color: [0xff, 0x66, 0x2a],
      scale: [-0.25, 0.25],
      offset: [-0.25, 0.25],
      angle: PI / 2,
    },
    {
      color: [0xff, 0xa2, 0x2a],
      scale: [-0.5, 0.5],
      offset: [0.25, 0.25],
      angle: 0,
    },
    {
      color: [0x82, 0xac, 0x26],
      scale: [0.5, 0.5],
      offset: [-0.25, -0.25],
      angle: PI,
    },
    {
      color: [0x4f, 0x3f, 0x84],
      scale: [0.5, 0.5],
      offset: [0.25, -0.25],
      angle: PI / 2,
    },
  ];

  function draw_border() {
    ctx.beginPath();
    ctx.lineTo(L, 0);
    ctx.lineTo(L, L);
    ctx.lineTo(0, L);
    ctx.lineTo(0, 0);
    ctx.closePath();
    ctx.stroke();
  }

  function draw() {
    draw_border();
    
    draw_figure();
  }

  function draw(x, y, sx, sy, a, color) {
    ctx.save();
    ctx.beginPath();
    ctx.translate(x, y)
    ctx.rotate(a)
    ctx.translate(-x, -y)
    let s = L / 4;
    for (let row = 0; row < FIGURE_LENGTH; ++row) {
      for (let col = 0; col < FIGURE_LENGTH; ++col) {
        if (FIGURE_MASK[row][col] == 0) continue;
        ctx.rect(x + sx * s * (col - 2), y + sy * s * (row - 2), s * sx, s * sy);
      }
    }
    ctx.closePath();
    let oldFillStyle = ctx.fillStyle;
    ctx.fillStyle = color;
    ctx.fill();
    ctx.fillStyle = oldFillStyle;
    ctx.restore();
  }

  const ANIMATION_TIME_SECONDS = 2 * 1000;

  let t_prev = Date.now()
  let t_now = Date.now()
  let t_elapsed = 0

  let piece_index = 0

  // initial configuration

  let x0 = 0, y0 = 0, sx0 = 1, sy0 = 1, a0 = 0, c0 = [0,0,0]
  let x1 = x0 + L * FRACTAL_CONFIG[piece_index].offset[0];
  let y1 = y0 + L * FRACTAL_CONFIG[piece_index].offset[1];
  let sx1 = FRACTAL_CONFIG[piece_index].scale[0];
  let sy1 = FRACTAL_CONFIG[piece_index].scale[1];
  let a1 = FRACTAL_CONFIG[piece_index].angle;
  let c1 = FRACTAL_CONFIG[piece_index].color;
  let x = x0, y = y0, sx = sx0, sy = sy0, a = a0, c = [...c0], color = '#000000'

  const piece_component = $("#piece");

  piece_component.on("input", function () {
    t_elapsed = 0;
    piece_index = piece_component.val();
  
    x1 = x0 + L * FRACTAL_CONFIG[piece_index].offset[0];
    y1 = y0 + L * FRACTAL_CONFIG[piece_index].offset[1];
    sx1 = FRACTAL_CONFIG[piece_index].scale[0];
    sy1 = FRACTAL_CONFIG[piece_index].scale[1];
    a1 = FRACTAL_CONFIG[piece_index].angle;
    c1 = FRACTAL_CONFIG[piece_index].color;
    x = x0,
    y = y0,
    sx = sx0,
    sy = sy0,
    a = a0,
    c = [...c0],
    color = "#000000";
  });

  function update(dt) {
    t_elapsed = t_elapsed + dt;

    if (t_elapsed > ANIMATION_TIME_SECONDS) {
      // don't animate if animation timer ran out
      return;
    }

    // lerp time [0, 1]
    let t = Math.min(t_elapsed / ANIMATION_TIME_SECONDS, 1);
    
    x = x1 * t + x0 * (1 - t)
    y = y1 * t + y0 * (1 - t)
    sx = sx1 * t + sx0 * (1 - t)
    sy = sy1 * t + sy0 * (1 - t)
    a = a1 * t + a0 * (1 - t)

    c[0] = c1[0] * t + c0[0] * (1 - t)
    c[1] = c1[1] * t + c0[1] * (1 - t)
    c[2] = c1[2] * t + c0[2] * (1 - t)

    let cs = c.map(Math.trunc).map((v) => v.toString(16).padStart(2, "0"));
    color = "".concat('#', cs[0], cs[1], cs[2])
  }

  ctx.translate(L / 2, L / 2);
  ctx.rotate(PI / 2);

  setInterval(function() {
    t_now = Date.now()
    let dt = t_now - t_prev
    ctx.clearRect(-canvas.width / 2, -canvas.height/2, canvas.width, canvas.height);
    update(dt)
    draw(x, y, sx, sy, a, color);
    t_prev = t_now
  }, 5)

})