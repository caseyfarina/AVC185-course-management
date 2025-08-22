using System.Collections;
using System.Collections.Generic;
using UnityEngine;



public class tankAnimationController : MonoBehaviour {
	
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
				anim.Play("rightTurn",-1,0);
		
			}
			if (Input.GetAxisRaw("HorizontalUI") < 0) {
			
				//play the animation in the animator component MUST BE NAMED CORRECTLY
				anim.Play("leftTurn",-1,0);
		
			}
			if (Input.GetAxisRaw("VerticalUI") < 0) {
			
				//play the animation in the animator component MUST BE NAMED CORRECTLY
				anim.Play("forwardMove",-1,0);
		
			}
			if (Input.GetAxisRaw("VerticalUI") > 0) {
			
				//play the animation in the animator component MUST BE NAMED CORRECTLY
				anim.Play("backwardsMove",-1,0);
		
			}
		}
	}
}

