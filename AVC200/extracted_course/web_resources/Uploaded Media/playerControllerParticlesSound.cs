using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using TMPro;
using UnityEngine.SceneManagement;

public class playerControllerParticlesSound : MonoBehaviour
{
    public float speed = 5f;
    public TextMeshProUGUI countText;
    public GameObject winTextObject;
    public GameObject TryAgainObject;
    public int winNumber = 10;
    public float loseHeight = -19f;
    public float ImpactVolume = .5f;
    public float ImpactVolumeThreshold = 1f;
    public AudioClip Impact;
    public float pickUpVolume = .5f;
    public AudioClip pickUp;
    public GameObject explosionParticle;
    public string PickUpTag = "PickUp";

    private AudioSource thisAudioSource;
    private int count = 0;
    private Rigidbody rb;
    private float movementX;
    private float movementY;
    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        SetCountText();
        if(winTextObject != null)
        {
            winTextObject.SetActive(false);
        }

        if (TryAgainObject != null)
        {
            TryAgainObject.SetActive(false);
        }
            
        
       
        thisAudioSource = transform.GetComponent<AudioSource>();
        
    }

    void OnMove(InputValue movementValue)
    {
        Vector2 movementVector = movementValue.Get<Vector2>();
        movementX = -movementVector.x;
        movementY = -movementVector.y;
    }

    void FixedUpdate()
    {
        Vector3 movement = new Vector3(movementX, 0.0f, movementY);
        rb.AddForce(movement*speed);

        if(transform.position.y < loseHeight)
        {
            Invoke("RestartLevel", 2);
            if(TryAgainObject != null)
            {
                TryAgainObject.SetActive(true);
            }
            
        }
    }

    void RestartLevel()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.gameObject.CompareTag(PickUpTag))
        {
            other.gameObject.SetActive(false);
            count += 1;

            if(thisAudioSource != null)
            {
                thisAudioSource.volume = pickUpVolume;
                thisAudioSource.PlayOneShot(pickUp);
            }

            if(explosionParticle != null)
            {
                Instantiate(explosionParticle, transform.position, Quaternion.identity);
            }
            //make a new explosion
            
            
            SetCountText();
        }
    }

    private void OnCollisionEnter(Collision collision)
    {
        float collisionForce = collision.impulse.magnitude / Time.fixedDeltaTime;
        if (collisionForce > ImpactVolumeThreshold)
        {
            if (thisAudioSource != null)
            {
                thisAudioSource.volume = ImpactVolume;
                thisAudioSource.PlayOneShot(Impact);
            }
        }
    }

    void SetCountText()
    {
        countText.text = "Count: " + count.ToString();

        if (count >= winNumber)
        {
            if (winTextObject != null)
            { 
            // Set the text value of your 'winText'
            winTextObject.SetActive(true);
            }
        }
    }
}
