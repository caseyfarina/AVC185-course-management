using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using StarterAssets;

public class thirdPersonAnimationControllerStarterAssets : MonoBehaviour
{
    public GameObject PlayerObject;
    public string jumpAnimationClipName = "jump"; 
    private CharacterController characterController;
    private ThirdPersonController playerController;
    private Animator thisAnimator;

    private bool previousJumpState;
   
    // Start is called before the first frame update
    void Start()
    {
        playerController = PlayerObject.GetComponent<ThirdPersonController>();
        characterController = PlayerObject.GetComponent<CharacterController>();
        thisAnimator = GetComponent<Animator>();

    }

    // Update is called once per frame
    void Update()
    {
      
        
        
        if(playerController.Grounded == false && playerController.Grounded != previousJumpState)
            {


                   thisAnimator.Play(jumpAnimationClipName);
            }
    
        previousJumpState = playerController.Grounded;

        float normalizedVelocity = characterController.velocity.magnitude * Time.deltaTime * 10f;
        Debug.Log(normalizedVelocity);
        
        thisAnimator.SetFloat("_velocity", normalizedVelocity);
    }
}
