const canvas = $("#canvas")[0]
const ctx = canvas.getContext("2d")

const canvas_center = [canvas.width, canvas.height].map((x) => x / 2)

const gear_count = 2
const gear_sizes = [0,0]
const gear_radii = gear_sizes.map(x => x / 2)
const gear_placement_angles_deg = [0, 0]

const large_gear_svg = new Image()
large_gear_svg.src = "assets/large-gear-debug.svg"
const large_scale = 4
const large_r = large_gear_svg.width * large_scale / 2
let large_angle = 0

const small_gear_svg = new Image()
small_gear_svg.src = "assets/small-gear-debug.svg"
const small_scale = 1.25 // 1.2 for real gears, 1.25 for debug gears
const small_r = small_gear_svg.width * small_scale / 2
let small_angle = 0//.46

const magic_ratio_constant = 1.17155 // 1.17155 for debug gears, 

let t_current = Date.now()
let t_last = Date.now()

const large_outside_radius_ratio = 1
const large_inside_radius_ratio = 223.5/256;
const large_pitch_radius_ratio = (large_outside_radius_ratio + large_inside_radius_ratio) / 2;

const small_outside_radius_ratio = 1
const small_inside_radius_ratio = 152/256;
const small_pitch_radius_ratio = (small_outside_radius_ratio + small_inside_radius_ratio) / 2;

const large_position = canvas_center
const gear_distance = large_pitch_radius_ratio * large_r + small_pitch_radius_ratio * small_r;
const small_position = [
  large_position[0] + gear_distance * Math.cos(0),
  large_position[1] + gear_distance * Math.sin(0),
]

const large_angular_speed = 2 * Math.PI / 30000

function draw_large_gear(center_position, angle, draw_debug=false)
{
  draw_gear(center_position, large_r, angle, large_gear_svg)
  if(draw_debug)
  {
    draw_gear_debug_info(
      center_position, 
      large_r, 
      large_inside_radius_ratio,
      large_pitch_radius_ratio,
      large_outside_radius_ratio
    )
  }
}

function draw_small_gear(center_position, angle, draw_debug=false)
{
  draw_gear(center_position, small_r, angle, small_gear_svg)
  if(draw_debug)
  {
    draw_gear_debug_info(
      center_position, 
      small_r, 
      small_inside_radius_ratio,
      small_pitch_radius_ratio,
      small_outside_radius_ratio
    )
  }
}

function draw_gear(center_position, radius, angle, img)
{
  let x = center_position[0], y = center_position[1]
  ctx.save()
  ctx.translate(x, y);
  ctx.rotate(angle);
  ctx.translate(-x, -y);
  ctx.drawImage(img, x - radius, y - radius, 2 * radius, 2 * radius);
  ctx.restore();
}

function draw_circle(p, r, fill_color, outline_color)
{
  ctx.save()
  ctx.beginPath();
  ctx.arc(p[0], p[1], r, 0, 2 * Math.PI, true);
  ctx.closePath();

  if(fill_color != null)
  {
    let oldStyle = ctx.fillStyle;
    ctx.fillStyle = fill_color;
    ctx.fill();
    ctx.fillStyle = oldStyle;
  }
  if(outline_color != null)
  {
    let oldStyle = ctx.strokeStyle;
    ctx.strokeStyle = outline_color;
    ctx.stroke();
    ctx.strokeStyle = oldStyle;
  }
  ctx.restore();
}

function draw_gear_debug_info(
  center_position, 
  radius,
  inside_radius_ratio,
  pitch_radius_ratio,
  outside_radius_ratio)
{
  //draw_circle(center_position, inside_radius_ratio * radius, "#ff000088", null);
  draw_circle(center_position, pitch_radius_ratio * radius, null, "#00ff00");
  draw_circle(center_position, outside_radius_ratio * radius, null, "#00ffff");
}

function draw()
{
  t_current = Date.now()
  const dt = t_current - t_last
  t_last = t_current

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  let da = large_angular_speed * dt
  large_angle += da
  small_angle += magic_ratio_constant * -da * large_r / small_r

  draw_large_gear(large_position, large_angle);
  draw_small_gear(small_position, small_angle);
}

setInterval(draw, 10)