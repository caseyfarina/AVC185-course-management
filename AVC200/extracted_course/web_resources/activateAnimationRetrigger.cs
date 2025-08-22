using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class activateAnimationRetrigger : MonoBehaviour
{
    //public Animation animationToTrigger;
    public GameObject animatingObject;
    public string animationName;
    //public bool backwards;
    private Animator thisAnimator;
    private bool flipthing = false;

    public Material triggeredMaterial;
    private MeshRenderer thisMesh;
    // Start is called before the first frame update
    void Start()
    {
        thisAnimator = animatingObject.GetComponent < Animator > ();

        if(GetComponent<MeshRenderer>() != null)
        {
            thisMesh = GetComponent<MeshRenderer>();
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    
    void OnTriggerEnter(Collider other)
    {
       
            // ..and if the game object we intersect has the tag 'Pick Up' assigned to it..
            if (other.gameObject)
            {
                    thisAnimator.Play(animationName, -1, 0);
                    flipthing = true;
                if (GetComponent<MeshRenderer>() != null)
                {
                    thisMesh.material = triggeredMaterial;
                }
            }
        } 


}
