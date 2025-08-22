using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class pickupSoundParticle : MonoBehaviour
{
    public string pickupTag = "PickUp";
    AudioSource thisAudio;
    public ParticleSystem thispart;

    // Start is called before the first frame update
    void Start()
    {
        thisAudio = GetComponent<AudioSource>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnTriggerEnter(Collider other)
    {
        // ..and if the game object we intersect has the tag 'Pick Up' assigned to it..
        if (other.gameObject.CompareTag(pickupTag))
        {
            thisAudio.Play();

            thispart.Play();


        }
    }
}
