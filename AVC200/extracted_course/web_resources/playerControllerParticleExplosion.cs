using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using TMPro;
using UnityEngine.SceneManagement;

public class playerControllerParticleExplosion : MonoBehaviour
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
        winTextObject.SetActive(false);
        TryAgainObject.SetActive(false);
       
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
            TryAgainObject.SetActive(true);
        }
    }

    void RestartLevel()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.gameObject.CompareTag("PickUp"))
        {
            other.gameObject.SetActive(false);
            count += 1;


            thisAudioSource.volume = pickUpVolume;
            thisAudioSource.PlayOneShot(pickUp);

            //make a new explosion
            Instantiate(explosionParticle, transform.position, Quaternion.identity);
            
            SetCountText();
        }
    }

    private void OnCollisionEnter(Collision collision)
    {
        float collisionForce = collision.impulse.magnitude / Time.fixedDeltaTime;
        if (collisionForce > ImpactVolumeThreshold)
        {
            thisAudioSource.volume = ImpactVolume;
            thisAudioSource.PlayOneShot(Impact);
        }
    }

    void SetCountText()
    {
        countText.text = "Count: " + count.ToString();

        if (count >= winNumber)
        {
            // Set the text value of your 'winText'
            winTextObject.SetActive(true);
        }
    }
}
