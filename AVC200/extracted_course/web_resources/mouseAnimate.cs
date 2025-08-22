// Change the mesh color in response to mouse actions.

using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class mouseAnimate : MonoBehaviour
{

  
    Animator anim;
    [Header("mouse Enter Animation Name")]

    public string animationNameOver;

    [Header("mouse Leave Animation Name")]

    public string animationNameExit;

    void Start()
    {
      
        anim = GetComponent<Animator>();
    }

    // The mesh goes red when the mouse is over it...
    void OnMouseEnter()
    {

    
        anim.Play(animationNameOver);
    }

    // ...the red fades out to cyan as the mouse is held over...
    void OnMouseOver()
    {
  
    }

    // ...and the mesh finally turns white when the mouse moves away.
    void OnMouseExit()
    {
        anim.Play(animationNameExit);
    }
}
