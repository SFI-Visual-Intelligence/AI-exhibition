// Copyright 2017 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
// implied. See the License for the specific language governing
// permissions and limitations under the License.
/**
 * Author: David Ha <hadavid@google.com>
 *
 * @fileoverview Basic p5.js sketch to show how to use sketch-rnn
 * to finish the user's incomplete drawing, and loop through different
 * endings automatically.
 */
var sketch = function( p ) { 
  "use strict";

  // params
  const params = initialise_param_object();
  // tracking mouse  touchpad
  const tracking = {
    down: false,
    x: 0,
    y: 0
  };  

  let line_x = 0;
  var start, end, delta_time;
  
  //

  p.setup = function() {

    init_model(params, model_raw_data);
    init_screen_size(p, params);

    draw_gui(p, params);
    restart(p, params);
    p.createCanvas(params.screen_width, params.screen_height);
    p.frameRate(60);
    //clear_screen(p);
    console.log('ready.');
    
  };


  p.draw = function() {

    draw_the_stuff(p, params, tracking);
      /*
      p.background(204);
      line_x = line_x + 1;
      if (line_x > p.width) {
        line_x = 0;
      }
      p.line(line_x, 0, line_x, p.height)
      */
  }
  
};

  
var custom_p5 = new p5(sketch, 'sketch');



function initialise_param_object(){
  const params = new Object();

  params.class_list = ['bicycle',
          'butterfly',
          'pig',
          'flower', 
          'truck',
          'face'];

  // Finished drawing delay
  params.clear_delay = 1000;
  params.timer = null;

  // local-datasets relpath
  params.model_param_path = "./dataset/";

  // sketch_rnn model
  params.model = null;
  params.model_data = null;
  params.temperature = 0.25;
  params.min_sequence_length = 5;

  params.model_pdf = null; // store all the parameters of a mixture-density distribution
  params.model_state = null;
  params.model_state_orig = null;
  params.model_prev_pen = null;
  params.model_dx = null;
  params.model_dy = null;
  params.model_pen_down = null; 
  params.model_pen_up = null;
  params.model_pen_end = null;
  params.model_x = null;
  params.model_y = null;
  params.model_is_active = null;

  // variables for the sketch input interface.
  params.pen = null;
  params.prev_pen = null;
  params.x = null 
  params.y = null; // absolute coordinates on the screen of where the pen is
  params.start_x = null;
  params.start_y = null;
  params.has_started = null; // set to true after user starts writing.
  params.just_finished_line = null;
  params.epsilon = 2.0; // to ignore data from user's pen staying in one spot.
  params.raw_lines = null;
  params.current_raw_line = null;
  params.strokes = null;
  params.line_color = null;
  params.predict_line_color = null;

  // UI
  params.screen_width = null;
  params.screen_height = null;
  params.buttonheight = null;
  params.buttonwidth = null;
  params.temperature_slider = null;
  params.line_width = 12;
  params.screen_scale_factor = 3.0;

  // dom
  params.reset_button = null;
  params.model_sel = null;
  params.random_model_button = null;
  params.button_height = 100;
  params.button_width = 200;
  params.text_title = null;
  params.text_temperature = null;

  // model selection
  params.font_scale = 8;
  params.potential_draw_button_list = [];

  params.title_text = "sketch-rnn predictor.";


  return params;
};


/*
 *
 *
 * BEGIN INIT FUNCTIONS
 *
 *
*/


function init_model(params, initial_model_raw_data){
  ModelImporter.set_init_model(initial_model_raw_data);
  ModelImporter.set_model_url(params.model_param_path);


  params.model_data = ModelImporter.get_model_data();
  params.model = new SketchRNN(params.model_data);
  params.model.set_pixel_factor(params.screen_scale_factor); 
}


function init_screen_size(p, params){
  params.screen_width = 1080; 
  params.screen_height = 1920;
}



/*
 *
 *
 * END INIT FUNCTIONS
 *
 *
*/


/*
 *
 *
 * BEGIN GUI FUNCTIONS
 *
 *
*/


function set_title_text(params, new_text) {
  params.title_text = new_text.split('_').join(' ');
  params.text_title.html(params.title_text);

  params.text_title.position(params.screen_width/2-12* params.title_text.length/2+10, 0);
};

var update_temperature_text = function(params) {
    var the_color="rgba("+Math.round(255*params.temperature)+",0,"+255+",1)";
    params.text_temperature.style("color", the_color); // ff990a
    params.text_temperature.html(""+Math.round(params.temperature*100));
  };


function draw_gui(p, params){
  // title
  params.text_title = p.createP(params.title_text);
  params.text_title.style("font-family", "Courier New");
  params.text_title.style("font-size", "20");
  params.text_title.style("color", "#3393d1"); // ff990a
  set_title_text(params, params.title_text);

  // temperature text
  params.text_temperature = p.createP();
  params.text_temperature.style("font-family", "Courier New");
  params.text_temperature.style("font-size", "16");
  params.text_temperature.position(params.screen_width-40, params.screen_height-64);

  update_temperature_text(params);

  //buttons
  generate_buttons(p, params);
};


function generate_buttons(p, params){

  var model_sel_event = function(model_sel) {
    var c = model_sel;
    var model_mode = "gen";
    console.log("user wants to change to model "+c);
    var call_back = function(new_model) {
      params.model = new_model;
      params.model.set_pixel_factor(params.screen_scale_factor);
      encode_strokes(p, params, params.strokes);
      clear_screen(p);
      draw_example(p, params, params.strokes);
      set_title_text(params, 'draw '+params.model.info.name+'.');
    }
    set_title_text(params, 'loading '+c+' model...');
    console.log('loading '+c+' model...');
    ModelImporter.change_model(params.model, c, model_mode, call_back);
  };

/* no random for Unreal GUI
  var random_model_button_event = function() {
    var item = Math.floor(Math.random() * params.class_list.length);
    model_sel = params.class_list[item];
    restart(p, params);
    model_sel_event(model_sel);
  };
*/

  var reset_button_event = function() {
    restart(p, params);
    clear_screen(p);
  };


  var model_sel_event_wrapper = function() {
    
    model_sel = this.value();
    model_sel_event(model_sel);
    reset_button_event();
  };

  var temperature_slider_event = function() {
    params.temperature = params.temperature_slider.value()/100;
    clear_screen(p);
    //draw_example(params.strokes, params.start_x, params.start_y, params.line_color);
    update_temperature_text(params);
  };


  var longest_draw_name = 0;
  var draw_name;
  var draw_button_shift;
  var draw_button_position;
  var buttonheight = 154;
  var buttonwidth = 154;

  reset_button = p.createButton('clear drawing');
  reset_button.position(25, 1900 - buttonheight*2);
  reset_button.size(1030, buttonheight);
  reset_button.mousePressed(reset_button_event); // attach button listener

  // random model buttom
  //random_model_button = p.createButton('random');
  //random_model_button.position(117, params.screen_height-27-27);
  //random_model_button.mousePressed(random_model_button_event); // attach button listener



  for (var i=0;i<params.class_list.length;i++) {
    if (params.class_list[i].length > longest_draw_name){
      longest_draw_name = params.class_list[i].length;
    }
  }
  draw_button_position = 27;
  draw_button_shift = 20;
  for (var i=0;i<params.class_list.length;i++) {

    draw_name = params.class_list[i];
    
    params.potential_draw_button_list[i] = p.createButton(draw_name, draw_name);
    params.potential_draw_button_list[i].position(draw_button_position, 1920 - buttonheight);
    params.potential_draw_button_list[i].size(buttonwidth, buttonheight);
    params.potential_draw_button_list[i].mousePressed(model_sel_event_wrapper);
    draw_button_position += (draw_button_shift + buttonwidth);
  }
/*
  // temp
  params.temperature_slider = p.createSlider(1, 100, params.temperature*100);
  params.temperature_slider.position(0*params.screen_width/2-10*0+10, params.screen_height-27);
  params.temperature_slider.style('width', params.screen_width/1-25+'px');
  params.temperature_slider.changed(temperature_slider_event);
*/
};


/*
 *
 *
 * END GUI FUNCTIONS
 *
 *
*/


/*
 *
 *
 * BEGIN DRAWING FUNCTIONS
 *
 *
*/


function encode_strokes(p, params, sequence){
  params.model_state_orig = params.model.zero_state();

  if (sequence.length <= params.min_sequence_length) {
      return;
    }

  params.model_state_orig = params.model.update(params.model.zero_input(), params.model_state_orig);

  for (var i=0; i<sequence.length-1; i++){
    params.model_state_orig = params.model.update(sequence[i], params.model_state_orig);
  }

  restart_model(p, params, sequence);

  params.model_is_active = true;
}


function draw_example(p, params, example_strokes){
  var i;
  var x, y;
  var dx, dy;
  var pen_down, pen_up, pen_end;
  var prev_pen = [1, 0, 0];

  x = params.start_x;
  y = params.start_y;

  for(i=0; i<example_strokes.length; i++){
    // sample the next pen's states from our probability distribution
    [dx, dy, pen_down, pen_up, pen_end] = example_strokes[i];

    // end of drawing.
    if (prev_pen[2] == 1) { 
        break;
    }

    // only draw on the paper if the pen is touching the paper
    if (prev_pen[0] == 1) {
      p.stroke(params.line_color);
      p.strokeWeight(params.line_width);
      p.line(x, y, x+dx, y+dy); // draw line connecting prev point to current point.
    }

    // update the absolute coordinates from the offsets
    x += dx;
    y += dy;

    // update the previous pen's state to the current one we just sampled
    prev_pen = [pen_down, pen_up, pen_end];
  }

};


/*
 *
 *
 * END DRAWING FUNCTIONS
 *
 *
*/



/*
 *
 *
 * BEGIN RESTART FUNCTIONS
 *
 *
*/


function clear_screen(p) {
  p.background(50, 50, 50, 255);
  p.fill(50, 50, 50, 255);
};


function restart_model(p, params, sequence){
  params.model_state = params.model.copy_state(params.model_state_orig);

  var idx = params.raw_lines.length-1;
  var last_point = params.raw_lines[idx][params.raw_lines[idx].length-1];
  var last_x = last_point[0];
  var last_y = last_point[1];

  var sx = last_x;
  var sy = last_y;

  var dx, dy, pen_down, pen_up, pen_end;
  var s = sequence[sequence.length-1];

  params.model_x = sx;
  params.model_y = sy;

  dx = s[0];
  dy = s[1];

  pen_down = s[2];
  pen_up = s[3];
  pen_end = s[4];

  params.model_dx = dx;
  params.model_dy = dy;
  params.model_prev_pen = [pen_down, pen_up, pen_end];
}


function restart(p, params){
    params.line_color = p.color(p.random(64, 224), p.random(64, 224), p.random(64, 224));
    params.predict_line_color = p.color(p.random(64, 224), p.random(64, 224), p.random(64, 224));

    // make sure we enforce some minimum size of our demo
    params.screen_width = 1080;
    params.screen_height = 1695;

    params.pen = 0;
    params.prev_pen = 1;
    params.has_started = false; // set to true after user starts writing.
    params.just_finished_line = false;
    params.raw_lines = [];
    params.current_raw_line = [];
    params.strokes = [];
    // start drawing from somewhere in middle of the canvas
    params.x = params.screen_width/2.0;
    params.y = params.screen_height/2.0;
    params.start_x = params.x;
    params.start_y = params.y;
    params.has_started = false;

    params.model_x = params.x;
    params.model_y = params.y;
    params.model_prev_pen = [0, 1, 0];
    params.model_is_active = false;
};



/*
 *
 *
 * END RESTART FUNCTIONS
 *
 *
*/

 

/*
 *
 *
 * BEGIN FREEZE FINISHED DRAWING FUNCTIONS
 *
 *
*/

var stop_at_finished_drawing = function(p, params) {
    p.noLoop();
    params.timer = setTimeout(function() {
      p.loop();
      params.timer = null;
    }, params.clear_delay);
  };


function releaseTimeout(params){
  if (params.timer != null){
      clearTimeout(timer);
      p.loop()
      params.timer = null;
    }
}


/*
 *
 *
 * END FREEZE FINISHED DRAWING FUNCTIONS
 *
 *
*/


/*
 *
 *
 * BEGIN DEVICE CONTROLLER FUNCTIONS
 *
 *
*/


function deviceReleased (tracking) {
  "use strict";
  tracking.down = false;
}

function devicePressed(params, tracking, x, y) {
  if (y < (params.screen_height-60)) {
    tracking.x = x;
    tracking.y = y;
    if (!tracking.down) {
      tracking.down = true;
    }
  }
};

function deviceEvent(p, params, tracking) {
    if (p.mouseIsPressed) {
      devicePressed(params, tracking, p.mouseX, p.mouseY);
    } else {
      deviceReleased(tracking);
    }
  }


/*
 *
 *
 * END DEVICE CONTROLLER FUNCTIONS
 *
 *
*/


/*
 *
 *
 * BEGIN BEGIN DRAW LOOP FUNCTIONS
 *
 *
*/


function draw_the_stuff(p, params, tracking){
  deviceEvent(p, params, tracking);
  //pen is touching the paper
  if (tracking.down && (tracking.x > 0) && tracking.y < (params.screen_height-60)) { 
    record_user_drawing(p, params, tracking);
  }
  else{
    params.pen = 1;

    if (params.just_finished_line){
      pen_above_paper(p, params, tracking);
    }

    if (params.model_is_active) {
      the_model_has_taken_over(p, params);
    } 
  }
  params.prev_pen = params.pen;
}

function record_user_drawing(p, params, tracking){
  // Asserting initial drawing
  if (params.has_started == false){
    params.has_started = true;

    params.x = tracking.x;
    params.y = tracking.y;

    params.start_x = params.x;
    params.start_y = params.y;

    params.pen = 0;
  }
  var dx0 = tracking.x - params.x;
  var dy0 = tracking.y - params.y;

  if (dx0 * dx0 + dy0 * dy0 > params.epsilon * params.epsilon){
    var dx = dx0;
    var dy = dy0;
    params.pen = 0;

    if (params.prev_pen == 0){
      p.stroke (params.line_color);
      p.strokeWeight(params.line_width);
      p.line(params.x, params.y, params.x+dx, params.y+dy);

    }

    // update the absolute coordinates from the offsets
    params.x += dx;
    params.y += dy;

    // update raw_lines
    params.current_raw_line.push([params.x, params.y]);
    params.just_finished_line = true;
  }
}


function pen_above_paper(p, params, tracking){ 
  var current_raw_line_simple = DataTool.simplify_line(params.current_raw_line);
  var idx, last_point, last_x, last_y;

  if (current_raw_line_simple.length > 1) {

    if (params.raw_lines.length === 0) {
      last_x = params.start_x;
      last_y = params.start_y;
    }
    else {
      idx = params.raw_lines.length - 1;
      last_point = params.raw_lines[idx][params.raw_lines[idx].length-1];
      last_x = last_point[0];
      last_y = last_point[1]; 
    }

    var stroke = DataTool.line_to_stroke(current_raw_line_simple, [last_x, last_y]);
    params.raw_lines.push(current_raw_line_simple);
    params.strokes = params.strokes.concat(stroke);


    //initialize rnn
    encode_strokes(p, params, params.strokes);

    // redraw simplified strokes
    clear_screen(p);
    draw_example(p, params, params.strokes)
  }
  else {
    if (params.raw_lines.length === 0) {
      params.has_started = false;
    }
  }

  params.current_raw_line = [];
  params.just_finished_line = false
}


function the_model_has_taken_over(p, params) {
  params.model_pen_down = params.model_prev_pen[0];
  params.model_pen_up = params.model_prev_pen[1];
  params.model_pen_end = params.model_prev_pen[2];

  params.model_state = params.model.update([
      params.model_dx,
      params.model_dy,
      params.model_pen_down,
      params.model_pen_up,
      params.model_pen_end],
      params.model_state
    );

  params.model_pdf = params.model.get_pdf(params.model_state);


  [params.model_dx,
   params.model_dy,
   params.model_pen_down,
   params.model_pen_up,
   params.model_pen_end] = params.model.sample(params.model_pdf, params.temperature);

  if (params.model_pen_end === 1){
    restart_model(p, params, params.strokes);

    params.predict_line_color = p.color(p.random(64, 224), p.random(64, 224), p.random(64, 224));
    clear_screen(p);
    draw_example(p, params, params.strokes);
  }
  else {

    if (params.model_prev_pen[0] === 1) {
      p.stroke(params.predict_line_color);
      p.strokeWeight(params.line_width);
      p.line(
        params.model_x,
        params.model_y,
        params.model_x + params.model_dx,
        params.model_y + params.model_dy
        );
    }

    params.model_prev_pen = [
      params.model_pen_down,
      params.model_pen_up,
      params.model_pen_end
      ];

    params.model_x += params.model_dx;
    params.model_y += params.model_dy;
  }
}


/*
 *
 *
 * END DRAW LOOP FUNCTIONS
 *
 *
*/


