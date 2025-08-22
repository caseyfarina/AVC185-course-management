using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class thirdPersonAnimationController : MonoBehaviour
{
    public GameObject PlayerObject;
    public string jumpAnimationClipName = "jump"; 
    private Rigidbody rBody;
    private PlayerMovementAdvancedOriginal playerMovement;
    private Animator thisAnimator;
    private PlayerMovementAdvancedOriginal.MovementState previousState;
    // Start is called before the first frame update
    void Start()
    {
        playerMovement = PlayerObject.GetComponent<PlayerMovementAdvancedOriginal>();
        rBody = PlayerObject.GetComponent<Rigidbody>();
        thisAnimator = GetComponent<Animator>();

    }

    // Update is called once per frame
    void Update()
    {
      
        
        
        if(playerMovement.state == PlayerMovementAdvancedOriginal.MovementState.air && playerMovement.state != previousState)
        {


            thisAnimator.Play(jumpAnimationClipName);
        }

        previousState = playerMovement.state;

        float normalizedVelocity = rBody.velocity.magnitude * Time.deltaTime * 10f;
        Debug.Log(normalizedVelocity);
        
        thisAnimator.SetFloat("_velocity", normalizedVelocity);
    }
}
