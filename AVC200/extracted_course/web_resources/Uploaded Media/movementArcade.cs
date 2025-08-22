using System.Collections;
using System.Collections.Generic;
using UnityEngine;



public class movementArcade : MonoBehaviour
{
    public float speed = 5f;

    Rigidbody2D rb;
    Vector2 movement;
    
    
    // Start is called before the first frame update
    void Start()
    {
        rb = transform.GetComponent<Rigidbody2D>();
        
    }

    // Update is called once per frame
    void Update()
    {
        movement.x = Input.GetAxisRaw("Horizontal");
        movement.y = Input.GetAxisRaw("Vertical");
    }

    private void FixedUpdate()
    {
        rb.MovePosition(rb.position + movement * speed * Time.fixedDeltaTime);
    }

    

}
