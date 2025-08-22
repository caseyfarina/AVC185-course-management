using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class _bumpPlayer : MonoBehaviour
{
    public float bounceForce = 20f;
    public UnityEvent onBumpEvent;
    public string playerTag = "Player";
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnCollisionEnter(Collision collision)
    {
        foreach (ContactPoint contact in collision.contacts)
        {
            // Debug.DrawRay(contact.point, contact.normal, Color.white);

            if (contact.otherCollider.CompareTag(playerTag))
            {

                contact.otherCollider.gameObject.GetComponent<Rigidbody>().AddForce(Vector3.Normalize(-contact.normal) * bounceForce, ForceMode.Impulse);

                onBumpEvent?.Invoke();

            };

            

        }
       
    }
}
