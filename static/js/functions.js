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
           $('#happiness-meter').html(data.value);
       }
    });
}

set_mobile_interaction = function() {
    $.get($.m_set_mobile_interaction_url, function(data) {
        // FIXME
        if (!data.error) {
            $('#mobile_interaction').find('span').text(data.mobile_interaction.toString());
        }
    });
}

get_mobile_interaction = function() {
    $.get($.m_get_mobile_interaction_url, function(data) {
        if (!data.error) {
            // FIXME
            $('#mobile_interaction').find('span').text(data.mobile_interaction.toString());
        }
    });
}

get_commands = function() {
    $.get($.m_get_commands_url, function ( data ) {
        if (!data.error && data.commands) {
            if (data.commands.length > 0) {
                $.each(data.commands, function(i, item) {
                    if ($('#command-count-'+item.pk).length > 0) {
                        $('#command-count-'+item.pk).html(item.total);
                    } else {
                        $('<li id="command-'+item.pk+'"><span>'+item.name+'</span> : <span id="command-count-'+item.pk+'">'+item.total+'</span></li>').appendTo('#command-list');
                    }
                });
            } else {
                $('#command-list').html('');
            }
        }
    });
}

get_chosen_commands = function() {
    $.get($.m_get_chosen_commands_url, function ( data ) {
        if (!data.error) {
            // Easy Mode
            if (data.commands) {
                if (data.commands.length > 0) {
                    $.each(data.commands, function(i, item) {
                        if ($('#chosen-command-'+item.pk).length == 0) {
                            $('<li id="chosen-command-'+item.pk+'"><span>'+item.name+'</span>').appendTo('#chosen-commands-list');
                        }
                    });
                } else {
                    $('#chosen-commands-list').html('');
                }
            }
            // Hard Mode
            if (data.actors) {
                if (data.actors.length > 0) {
                    $.each(data.actors, function(i, item) {
                        if ($('#chosen-command-'+item.pk).length == 0) {
                            $('<li id="chosen-command-'+item.pk+'"><span>'+item.name+': </span></li>').appendTo('#chosen-commands-list');
                            $.each(item.commands, function(i, c) {
                                $('<span id="command-'+ c.pk +'">'+c.name+', </span>').appendTo('#chosen-command-'+item.pk);
                            });
                        }
                        else {
                            $.each(item.commands, function(i, c) {
                                if ( $('#command-'+ c.pk).length == 0 ) {
                                    $('<span id="command-'+ c.pk +'">'+c.name+', </span>').appendTo('#chosen-command-'+item.pk);
                                }
                            });
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
            $('#happiness-meter').html(data.happiness_value);
        }
    });
}

reset_spectacle = function () {
    $.get($.m_reset_spectacle_url, function(data) {
        if (!data.error) {
            get_commands();
            get_chosen_commands();
            get_happiness_meter();
        }
    });
}

get_last_hard_message = function () {
    $.get($.m_get_last_hard_message_url, function(data) {
        if (!data.error) {
            $('#box-message').find('p').html(data.msg.text);
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
                        $('#command-'+item.pk).find('ul').append('<li class="carga"></li>');
                    }
                });
            }
        }
    });
}
