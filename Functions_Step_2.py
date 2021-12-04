#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on March 21 2021

Module for building the chance quality model and analyse the game

@author: Chloe Gobé
"""

# import librairies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

################################## STEP 2 ################################


def create_pitch(field_size=(106,68)):
    """
    Create a portion of a football pitch
    Inspiration : Drawing a Pitchmap - @FCPython

    Args:
        field_size (tuple, optional): Size of a football pitch (m). Defaults to (106,68).

    Returns:
        A plot of the soccer pitch
    """
    lenx = field_size[0]
    leny = field_size[1]/2
    
    #Create figure
    fig=plt.figure(figsize=(12,8))
    ax=fig.add_subplot(1,1,1)
    ax.set_facecolor('mediumseagreen')

    #Pitch Outline & Centre Line
    plt.plot([0,0],[-leny,leny], color="white")
    plt.plot([0,lenx],[leny,leny], color="white")
    plt.plot([lenx,lenx],[leny,-leny], color="white")
    plt.plot([lenx,0],[-leny,-leny], color="white")
    plt.plot([lenx/2,lenx/2],[leny,-leny], color="white")
    
    #Left Penalty Area
    plt.plot([16.5,16.5],[-20.15,20.15],color="white")
    plt.plot([0,16.5],[20.15,20.15],color="white")
    plt.plot([16.5,0],[-20.15,-20.15],color="white")
    
    #Right Penalty Area
    plt.plot([lenx-16.5,lenx],[20.15,20.15],color="white")
    plt.plot([lenx-16.5,lenx-16.5],[-20.15,20.15],color="white")
    plt.plot([lenx-16.5,106],[-20.15,-20.15],color="white")
    
    #Left 6-yard Box
    plt.plot([0,5.5],[9,9],color="white")
    plt.plot([5.5,5.5],[9,-9],color="white")
    plt.plot([5.5,0.5],[-9,-9],color="white")
    
    #Right 6-yard Box
    plt.plot([106,lenx-5.5],[9,9],color="white")
    plt.plot([lenx-5.5,lenx-5.5],[9,-9],color="white")
    plt.plot([lenx-5.5,106],[-9,-9],color="white")
    
    #Prepare Circles
    centreCircle = plt.Circle((lenx/2,0),9.15,color="white",fill=False)
    centreSpot = plt.Circle((lenx/2,0),0.8,color="white")
    leftPenSpot = plt.Circle((11,0),0.8,color="white")
    rightPenSpot = plt.Circle((lenx-11,0),0.8,color="white")
    
    #Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)
    
    #Prepare Arcs
    leftArc = Arc((11,0),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color="white")
    rightArc = Arc((lenx-11,0),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color="white")

    #Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)   
    
    #Display Pitch
    return fig, ax

def shot_angle_2(x, y):
    """Calculate the shot angle between the shooter and the goal posts
    Inspiration : @soccermatics

    Args:
        x (float): x coordinate of the shot
        y (float): y coordinate of the shot

    Returns:
        angle (float) : angle in radians
        
    Nota Bene : there is a slight change from step1 as the coordinates are a little bit changed    
    """
    x = 53 - abs(x)
    angle = np.arctan(7.32 *x /(x**2 + y**2 - (7.32/2)**2)) # A goal frame is 7,32m long
    if angle < 0:
        angle = np.pi + angle
    return angle

def distance_goal_2(x,y):
    """
    Calculate the distance between the shooter and the center of the goal (m)

    Args:
        x (float): x coordinate of the shot
        y (float): y coordinate of the shot

    Returns:
        float : distance b

    Nota Bene : there is a slight change from step1 as the coordinates are a little bit changed    
    """
    x = 53 - abs(x)
    return np.sqrt(x**2 + y**2)

def which_play_type(data):
    """
    Retrieve the play types from the Subtype information
    for the event that happens few moments before

    Args:
        data (dataframe): dataset of events (Metrica)

    Returns:
       list of tuples for shots taken off open play  : eg. [(id_shot1, Penalty), (id_shot2, Free kick)]
    """
    index_shots = list(data[data.Type == "SHOT"].index)
    return ([(idx, data.loc[idx-1]["Subtype"].title())
             for idx in index_shots
            if (data.loc[idx-1]["Subtype"] in ["PENALTY", "FREE KICK"])])
