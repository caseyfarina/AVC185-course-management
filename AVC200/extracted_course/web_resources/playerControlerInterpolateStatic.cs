using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DG.Tweening;

public class playerControlerInterpolateStatic : MonoBehaviour {
	public float tweenTime = 0.4f;
	public int stepSize = 1;
	private int xvalue;
	private int yvalue;
	public Animator anim;
	Rigidbody2D mybody;

	// Use this for initialization
	void Start () {
	
	//grab the animator component
		
		anim = gameObject.GetComponent<Animator>();
		mybody = gameObject.GetComponent<Rigidbody2D>();
		xvalue = (int)transform.position.x;
		yvalue = (int)transform.position.y;
	}
	
	// Update is called once per frame
	void Update () {
		 if (Input.GetKeyDown(KeyCode.DownArrow)){
			 yvalue = -stepSize +  ((int)mybody.position.y);
			 //play the animation in the animator component MUST BE NAMED CORRECTLY
			 anim.Play("player_backwards",-1,0);
			
			 //DOMoveY this is the move function
			 mybody.DOMoveY(yvalue, tweenTime).SetEase(Ease.OutBack);
	//		transform.DOMoveY(yvalue, tweenTime).SetEase(Ease.OutBack);
		 }
		 if (Input.GetKeyDown(KeyCode.UpArrow)){
			 yvalue = stepSize + ((int)mybody.position.y);
			 anim.Play("player_forward",-1,0);
			 mybody.DOMoveY(yvalue, tweenTime).SetEase(Ease.OutBack);
			//transform.DOMoveY(yvalue, tweenTime).SetEase(Ease.OutBack);
		 }
		 if (Input.GetKeyDown(KeyCode.LeftArrow)){
			 xvalue = -stepSize + ((int)mybody.position.x);
			// xvalue =  Mathf.RoundToInt(xvalue/3);
			 anim.Play("player_left",-1,0);
			  mybody.DOMoveX(xvalue, tweenTime).SetEase(Ease.OutBack);
			//transform.DOMoveX(xvalue, tweenTime).SetEase(Ease.OutBack);
		 }
		 if (Input.GetKeyDown(KeyCode.RightArrow)){
			anim.Play("player_right",-1,0);
			 xvalue  = stepSize + ((int)mybody.position.x);
			// xvalue =  Mathf.RoundToInt(xvalue/3);
			  mybody.DOMoveX(xvalue, tweenTime).SetEase(Ease.OutBack);
			//transform.DOMoveX(xvalue, tweenTime).SetEase(Ease.OutBack);
		 }
	}
}
