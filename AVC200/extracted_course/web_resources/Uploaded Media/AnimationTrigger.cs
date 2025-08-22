using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnimationTrigger: MonoBehaviour
{
    Animator animator;
    public GameObject ObjectToAnimate;
    public AnimationClip animationClip;
    // Start is called before the first frame update
    void Start()
    {
        animator = ObjectToAnimate.GetComponent<Animator>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnTriggerEnter(Collider other)
    {
        animator.Play(animationClip.name, -1,0f);
    }
}
