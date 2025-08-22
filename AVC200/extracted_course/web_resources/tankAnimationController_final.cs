using System.Collections;
using System.Collections.Generic;
using UnityEngine;



public class tankAnimationController_final : MonoBehaviour {
	
	public Animator anim;
	
	// Use this for initialization
	void Start () {
		//grab the reference to the animator controller
		anim = gameObject.GetComponent<Animator>();
	}
	
	// Update is called once per frame
	void Update () {
		if(Input.GetButtonDown("HorizontalUI")){
			if (Input.GetAxisRaw("HorizontalUI") > 0){
			
				//play the animation in the animator component MUST BE NAMED CORRECTLY
				anim.Play("Player1_Right Turn",-1,0);
		
			}
			if (Input.GetAxisRaw("HorizontalUI") < 0) {
			
				//play the animation in the animator component MUST BE NAMED CORRECTLY
				anim.Play("Player1_Left Turn",-1,0);
			}	
		}
		if(Input.GetButtonDown("VerticalUI")){
			
			if (Input.GetAxisRaw("VerticalUI") < 0) {
			
				//play the animation in the animator component MUST BE NAMED CORRECTLY
				anim.Play("Player1_Forward",-1,0);
		
			}
			if (Input.GetAxisRaw("VerticalUI") > 0) {
			
				//play the animation in the animator component MUST BE NAMED CORRECTLY
				anim.Play("Player1_Back",-1,0);
		
			}
			}
		}
	
}

