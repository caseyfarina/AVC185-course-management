using UnityEngine;

namespace Complete
{
    public class botHurt : MonoBehaviour
    {
      
        public float m_MaxDamage = 10f;                    // The amount of damage done if the explosion is centred on a tank.
		
        private ParticleSystem m_ExplosionParticles;        

        private void Start ()
        {
			m_ExplosionParticles = gameObject.GetComponent<ParticleSystem> ();
       
        }


        private void OnTriggerEnter (Collider other)
        {
			
			
			Rigidbody targetRigidbody = other.GetComponent<Rigidbody> ();
			 // If they don't have a rigidbody, go on to the next collider.
          

                

            // Find the TankHealth script associated with the rigidbody.
            TankHealth targetHealth = targetRigidbody.GetComponent<TankHealth> ();

            Debug.Log("hit");

                
			m_ExplosionParticles.Play ();
                // Deal this damage to the tank.
                targetHealth.TakeDamage (m_MaxDamage);
            

           
        }



    }
}
