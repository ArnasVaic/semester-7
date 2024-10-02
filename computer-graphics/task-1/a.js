$(function() {
  const canvas = $("#canvas")[0];
  const ctx = canvas.getContext("2d");
  const L = 512;

  let apply_color = false

  const PI = Math.PI;

  let TOTAL_STEPS = 0
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
      color: "#ff662a",
      scale: [-0.25, 0.25],
      offset: [-0.25, 0.25],
      angle: PI / 2,
    },
    {
      color: "#ffa22a",
      scale: [-0.5, 0.5],
      offset: [0.25, 0.25],
      angle: 0,
    },
    {
      color: "#82ac26",
      scale: [0.5, 0.5],
      offset: [-0.25, -0.25],
      angle: PI,
    },
    {
      color: "#4f3f84",
      scale: [0.5, 0.5],
      offset: [0.25, -0.25],
      angle: PI / 2,
    },
  ];

  let draw_index = 0

  function draw_figure() {
    ctx.save();
    ctx.beginPath();
    let s = L / 4;
    for (let row = 0; row < FIGURE_LENGTH; ++row) {
      for (let col = 0; col < FIGURE_LENGTH; ++col) {
        if (FIGURE_MASK[row][col] == 0) continue;
        ctx.rect(s * (col - 2), s * (row - 2), s, s);
      }
    }
    ctx.closePath();
    ctx.fill();

    // let oldFillStyle = ctx.fillStyle
    // ctx.fillStyle = "#ffffff"
    // ctx.scale(16, 16)
    // ctx.fillText(`${draw_index++}`, 0, 0);
    // ctx.scale(1/16, 1/16);
    // ctx.fillStyle = oldFillStyle

    draw_index++

    ctx.restore();
  }

  function draw_fractal(steps, piece_index, color) {
    if (steps == 0) {
      // draw index [0; total piece - 1] --?-> [0; 4]
      let total_pieces = Math.pow(4, TOTAL_STEPS)
      let color_index = Math.trunc(4 * draw_index / total_pieces);

      let oldFillStyle = ctx.fillStyle;
      ctx.fillStyle = apply_color ? FRACTAL_CONFIG[color_index].color : "#000000"; // apply_color ? FRACTAL_CONFIG[piece_index].color : '#000000';
      draw_figure();
      ctx.fillStyle = oldFillStyle
      return;
    }

    if (TOTAL_STEPS - 1 == steps)
    {
      FRACTAL_CONFIG.map((piece, index) => {
        ctx.save();
        let cos = Math.cos(piece.angle);
        let sin = Math.sin(piece.angle);
        ctx.transform(
          piece.scale[0] * cos,
          piece.scale[0] * sin,
          -piece.scale[1] * sin,
          piece.scale[1] * cos,
          L * piece.offset[0],
          L * piece.offset[1]
        );
        draw_fractal(steps - 1, index, piece.color);

        ctx.restore();
      })
      return
    }

    FRACTAL_CONFIG.map((piece, index) => {
      ctx.save();
      let cos = Math.cos(piece.angle);
      let sin = Math.sin(piece.angle);
      ctx.transform(
        piece.scale[0] * cos,
        piece.scale[0] * sin,
        -piece.scale[1] * sin,
        piece.scale[1] * cos,
        L * piece.offset[0],
        L * piece.offset[1]
      );
      draw_fractal(steps - 1, index, color);

      ctx.restore();
    });
  }

  function draw_border() {
    ctx.beginPath();
    ctx.lineTo(L, 0);
    ctx.lineTo(L, L);
    ctx.lineTo(0, L);
    ctx.lineTo(0, 0);
    ctx.closePath();
    ctx.stroke();
  }

  function draw(steps) {
    ctx.resetTransform();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    draw_border();
    ctx.translate(L / 2, L / 2);
    ctx.rotate(PI / 2);
    draw_fractal(steps, 0, FRACTAL_CONFIG[0].color);
  }

  draw(0);

  const slider = $("#steps")
  const colorbox = $('#color')

  slider.on("input", function () {
    draw_index = 0
    TOTAL_STEPS = slider.val();
    draw(TOTAL_STEPS);
  });

  colorbox.on('input', function() {
    draw_index = 0;
    apply_color = colorbox.is(":checked");
    draw(TOTAL_STEPS)
  })
})