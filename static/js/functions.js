/* -*- coding: utf-8 -*-
 * Copyright (C) 2012 Marcelo Jorge Vieira <metal@alucinados.com>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public
 * License along with this program; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */


get_happiness_meter = function() {
    $.get($.m_get_happiness_meter_url, function( data ) {
       if (!data.error) {
           $('#happiness-meter').css('height', data.value+'%');
       }
    });
}

set_mobile_interaction = function(duration) {
    $.get($.m_set_mobile_interaction_url, function(data) {
        // FIXME
        if (!data.error) {
            $('#mobile_interaction').find('span').text(data.mobile_interaction.toString());
            set_last_scene_duration(duration);
        }
    });
}

get_mobile_interaction = function() {
    $.get($.m_get_mobile_interaction_url, function(data) {
        if (!data.error) {
            if (data.mobile_interaction) {
                $('#mobile_interaction').html('<div id="mobile_interaction_on"></div>');
            } else {
                $('#mobile_interaction').html('');
            }
        }
    });
}

get_last_scene_duration = function () {
    $.get($.m_get_last_scene_duration_url, function ( data ) {
        if (!data.error) {
            if (data.scene.duration && data.scene.show) {

                $.get($.m_set_countdown_displayed_url, function ( d ) {
                    if (!d.error) {
                        $('#hard-countdown').countdown('destroy');
                        $('#hard-countdown').countdown({
                            until: data.scene.duration,
                            format: 'MS',
                            compact: true,
                        });
                        $('.dial').val(0).trigger('change');
                    }
                });

            }
            var countdown = $('#hard-countdown span').html();
            if (countdown) {
                var d = $('#hard-countdown span').html().split(':');
                if (d.length > 0) {
                    var duration = parseInt(parseInt(d[0])*60 + parseInt(d[1]));
                    var x = 100 - ((duration * 100) / data.scene.duration);
                    $('.dial').val(x).trigger('change');
                }
            }
        }
    });
}

set_last_scene_duration = function (duration) {
    if (duration) {
        $('#duration').val(duration);
        $.post($.m_set_last_scene_duration_url, $("#form-scene-duration").serialize() );
    }
}

get_commands = function() {
    $.get($.m_get_commands_url, function ( data ) {
        if (!data.error && data.commands) {
            if (data.commands.length > 0) {
                $.each(data.commands, function(i, item) {
                    if ($('#command-count-'+item.pk).length > 0) {
                        $('#command-count-'+item.pk).html(item.total);
                    } else {
                        $('<tr><td id="command-'+item.pk+'">'+item.name+'</td><td id="command-count-'+item.pk+'">'+item.total+'</td></tr>').appendTo('#command-list tbody');
                    }
                });
            } else {
                $('#command-list tbody tr').remove();
            }
        }
    });
}

get_chosen_commands = function(reload) {
    var reload = reload;
    $.get($.m_get_chosen_commands_url, function ( data ) {
        if (!data.error) {
            // Easy Mode
            if (data.command) {
                var block = false;
                var command = data.command;
                if ($('#chosen-command-'+command.pk).length == 0) {
                    $('#chosen-commands-list').html('<li id="chosen-command-'+command.pk+'"><span>'+command.name+'</span>');
                    block = true;
                }
                if (block && !reload) {
                    set_mobile_interaction();
                }
            } else {
                $('#chosen-commands-list').html('');
            }

            // Hard Mode
            if (data.actors) {
                if (data.actors.length > 0) {
                    $.each(data.actors, function(i, item) {
                        if ($('#chosen-command-'+item.pk).length == 0) {
                            $('<li id="chosen-command-'+item.pk+'"><span>'+item.name+': </span></li>').appendTo('#chosen-commands-list');
                            $('<span id="command-'+ item.command.pk +'">'+item.command.name+'</span>').appendTo('#chosen-command-'+item.pk);
                        }
                        else {
                            $('<span id="command-'+ item.command.pk +'">'+item.command.name+'</span>').appendTo('#chosen-command-'+item.pk);
                        }
                    });
                } else {
                    $('#chosen-commands-list').html('');
                }
            }
        }
    });
}

set_hard_chosen_commands = function (){
    $.get($.m_set_hard_chosen_commands_url, function ( data ) {
        if (!data.error) {
            set_mobile_interaction();
        }
    });
}

decrease_happiness = function() {
    $.get($.m_decrease_happiness_url, function(data) {
        if (data.happiness_value) {
            $('#happiness-meter').css('height', data.happiness_value+'%');
        }
    });
}

reset_spectacle = function () {
    $.get($.m_reset_spectacle_url, function(data) {
        if (!data.error) {
            setTimeout(function(){
                change_spectacle_mode();
                setTimeout(function(){
                    window.location.replace($.m_get_controller_url);
                }, 5000 ); // 5s
            }, 5000 ); // 5s
        }
    });
}

get_last_hard_message = function () {
    $.get($.m_get_last_hard_message_url, function(data) {
        if (!data.error && $.m_last_hard_message != data.msg.pk) {
            $('#box-message').find('p').html(data.msg.text);
            $.m_last_hard_message = data.msg.pk;
        }
    });
}

easy_mobile_commands = function() {
    $.get($.m_get_mobile_interaction_url, function(data) {
        if (!data.error) {
            if (data.mobile_interaction) {
                if ($('.command').hasClass('ativo')) {
                    $('.command').each(function() {
                        if (! $(this).hasClass('ativo')) {
                            $(this).addClass("blocked");
                            $(this).removeClass("inativo");
                        }
                    })
                } else {
                    $('.command').removeClass("blocked");
                    $('.command').addClass("inativo");
                }

            } else {
                $('.command').addClass("blocked");
                $('.command').removeClass("inativo");
                $('.command').removeClass("ativo");
            }
        }
    });
    $.get($.m_get_chosen_commands_total_url, function ( data ) {
        if (!data.error && data.commands) {
            if (data.commands.length > 0) {
                $.each(data.commands, function() {
                    if (this.total >= 3) {
                        $('#command-'+this.pk).addClass("blocked");
                        $('#command-'+this.pk).removeClass("ativo");
                        $('#command-'+this.pk).removeClass("inativo");
                    }
                    $('#command-'+this.pk).find('ul li').remove();
                    for (var x=1; x<= 3-this.total; x++) {
                        $('#command-'+this.pk).find('ul').append('<li class="carga"></li>');
                    }
                });
            }
        }
    });
}

change_spectacle_mode = function (){
    $.get($.m_change_spectacle_mode_url, function ( data ) {
        if (!data.error) {
            window.location.replace($.m_get_controller_url);
         }
    });
}

get_spectable_mode = function(url, url2){
    $.get($.m_get_spectable_mode_url, function ( data ) {
        if (!data.error && data.mode) {
            if ($.m_spectable_mode && $.m_spectable_mode != data.mode && data.mode != 3) {
                // FIXME
                if ($.m_spectable_mode == 3 && url2) {
                    window.location.replace(url2);
                } else {
                    window.location.replace(url);
                }
            }
            $.m_spectable_mode = data.mode;
         }
    });
}

show_chosen_commands = function(monitor){
    var monitor = monitor;
    $.get($.m_show_chosen_commands_url, function ( data ) {
        if (!data.error) {
            if ($.m_update_chosen_command != data.commands.pk) {
                if (monitor && data.commands.easy_monitor) {
                    $('#chosen-commands-list').hide();
                    $('#box-message').find('p').html(data.commands.easy_monitor);
                    // play sound
                    if (data.commands.sound) {
                        if ($('#sound-' + $.m_update_chosen_command).length >0) {
                            $('#sound-' + $.m_update_chosen_command)[0].pause();
                        }
                        html = '<audio id="sound-'+data.commands.pk+'"><source src="'+data.commands.sound+'" type="audio/mp3">Your browser does not support the audio element.</audio>';
                        $(html).appendTo('#box-message').find('p');
                        $('#sound-'+data.commands.pk)[0].play();
                    }
                } else if (data.commands.easy) {
                    $('#chosen-commands-list').hide();
                    $('#box-message').find('p').text(data.commands.easy);
                }
                $.m_update_chosen_command = data.commands.pk;
            } else if (data.commands.hard) {
                $('#box-message').show();
                $('#chosen-commands-list').show();
                $.each(data.commands.hard, function() {
                    var actor = '.'+this.actor.slug;
                    if ($(actor).length > 0) {
                        $(actor + ' .command').html(this.command.name);
                    } else {
                        $('<li class="'+this.actor.slug+'"><div class="monitor"><span class="actor">'+this.actor.name+':</span> '+'<span class="command">'+this.command.name+'</span></div></li>').appendTo('#chosen-commands-list');
                    }
                });
                if (monitor && $.m_scene_chosen_command != data.commands.scene.pk) {
                    $.each($('#chosen-commands audio[id^="sound-"]'), function() {
                        $('#'+this.id)[0].pause();
                        $('#'+this.id).remove();
                    });
                    $.each(data.commands.hard, function() {
                        if (this.command.sound) {
                            html = '<audio id="sound-'+this.command.pk+'"><source src="'+this.command.sound+'" type="audio/mp3">Your browser does not support the audio element.</audio>';
                            $(html).appendTo('#chosen-commands');
                            $('#sound-'+this.command.pk)[0].play();
                            $.m_scene_chosen_command = data.commands.scene.pk;
                        }
                    });
                }
            }
        }
    });
}

get_backside_projection_content = function() {
    $.get($.m_backside_projection_content_url, function ( data ) {
        if (!data.error && data.file) {
            // FIXME
            if ($.m_backside_projection_content_show != data.file) {
                if (data.archive_type == 'image') {
                    $(".content").html('<img src="'+data.file+'">');
                } else {
                    $(".content").html('<video autoplay="autoplay"><source src="'+data.file+'" type="video/ogg" />Your browser does not support the video tag.</video>');
                }
            }
            $.m_backside_projection_content_show = data.file;
        } else {
            $(".content").html('');
            $.m_backside_projection_content_show = '';
        }
    });
}

set_backside_projection_content = function () {
    $.post($.m_set_backside_projection_content_url, $("#backside-projection-form").serialize() );
}

get_bullets = function() {
    $.get($.m_get_frontal_projection_draw_list_bullet_url, function ( data ) {
        if (!data.error) {
            $('.command span').removeClass();
            $('.command span').addClass('score score-0');
            if (data.commands) {
                $.each(data.commands, function() {
                    $('.command span').removeClass('score-0');
                    $('#command-count-'+this.pk).addClass('score-'+this.draw);
                });
            }
        }
    });

    $.get($.m_get_chosen_commands_total_url, function ( data ) {
        if (!data.error && data.commands) {
            if (data.commands.length > 0) {
                $.each(data.commands, function() {
                    if (this.total >= 3 && $('#command-'+this.pk).length > 0) {
                        $('#command-'+this.pk).remove();
                    }
                });
            }
        }
    });
}

delete_logged_users = function() {
    $.get($.m_delete_logged_users_url, function(data) {
        if (!data.error) {
        }
    });
}
