using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class mouseOverObject : MonoBehaviour
{
    //When the mouse hovers over the GameObject, it turns to this color (red)
    
    public GameObject cameraParent;
    public GameObject closeUpCamera;
    public Material highlightMaterial;
    public GameObject UIObject;
    public AnimationClip animateOn;
    public AnimationClip animateOff;


    //list of cameras to enable slash disable
    List<Transform> objectCameras;

    //This stores the GameObject’s original color
    Color m_OriginalColor;

    //Get the GameObject’s mesh renderer to access the GameObject’s material and color
    MeshRenderer m_Renderer;
    Material originalMaterial;

    //turn off highlight on click
    bool overEnabled = true;

    Animator thisAnimator;

    bool currentlyActive = false;
    bool currentlyOver = false;
  

    void Start()
    {

        objectCameras = new List<Transform>();

        //Get all the child cameras
        GetRecursiveChildren(cameraParent.transform);

        

        //Fetch the mesh renderer component from the GameObject
        m_Renderer = GetComponent<MeshRenderer>();
        //Fetch the original color of the GameObject
        m_OriginalColor = m_Renderer.material.color;
        originalMaterial = m_Renderer.material;

  


        foreach (Transform thinglist in objectCameras)
        {
            thinglist.gameObject.SetActive(false);
        }


        if(UIObject != null)
        {
            thisAnimator = UIObject.GetComponent<Animator>();
        }
        
    }

    private void Update()
    {
        //was the mouse clicked off the object?
        if(Input.GetMouseButtonDown(0) && currentlyActive)
        {
            if (!currentlyOver)
            {
                if (UIObject != null)
                {
                    thisAnimator.Play(animateOff.name);
                }
            }
            
        }
    }

    void OnMouseOver()
    {
       //change the material to the highlight material once the object is moused over
        if (overEnabled)
        {
            m_Renderer.material = highlightMaterial;
        }

        currentlyOver = true;


    }

    void OnMouseExit()
    {
        // Reset the color of the GameObject back to normal
        //m_Renderer.material.color = m_OriginalColor;
        m_Renderer.material = originalMaterial;

        overEnabled = true;

        currentlyOver = false;

    }

    private void OnMouseDown()
    {
        currentlyActive = true;


        m_Renderer.material = originalMaterial;

        overEnabled = false;

        //turn off all the cameras
        foreach(Transform thinglist in objectCameras)
        {
            thinglist.gameObject.SetActive(false);
        }

        //check to make sure there is a closeUp Camera
        if(closeUpCamera != null)
        {
            //turn on the respective camera
            closeUpCamera.SetActive(true);

        }


        if(UIObject != null)
        {
            thisAnimator.Play(animateOn.name);
        }
        
       
    }

   


    //custom function from https://github.com/aniketrajnish/get-all-children-of-a-gameobject
    private void GetRecursiveChildren(Transform parenttransform)
    {
        foreach (Transform child in parenttransform)
        {
            objectCameras.Add(child.transform);
            if (child.transform.childCount > 0)
            {
                GetRecursiveChildren(child);
            }
        }
    }

    public void DisableAllCameras()
    {
        //turn off all the cameras
        foreach (Transform thinglist in objectCameras)
        {
            thinglist.gameObject.SetActive(false);

            if (UIObject != null)
            {
                if (thisAnimator.GetCurrentAnimatorStateInfo(0).IsName(animateOn.name))
                {

                    thisAnimator.Play(animateOff.name);
                }
            }
        }
    }
}
