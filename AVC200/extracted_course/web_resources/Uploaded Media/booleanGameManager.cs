using UnityEngine;
using UnityEngine.Events;

public class booleanGameManager : MonoBehaviour
{
    public UnityEvent onAllTrue;

    public bool bool1 = false;
    public bool bool2 = false;
    public bool bool3 = false;
    public bool bool4 = false;
    private bool gate = true;

    public void SetBool1(bool value)
    {
        bool1 = value;
        CheckBooleans();
    }

    public void SetBool2(bool value)
    {
        bool2 = value;
        CheckBooleans();
    }

    public void SetBool3(bool value)
    {
        bool3 = value;
        CheckBooleans();
    }

    public void SetBool4(bool value)
    {
        bool4 = value;
        CheckBooleans();
    }

    private void CheckBooleans()
    {
        if (bool1 && bool2 && bool3 && bool4 && gate)


        {
            // Check if the event has subscribers before invoking
            
                onAllTrue.Invoke();
            gate = false;

            
        }
    }

    private void Update()
    {

       CheckBooleans();
    }
}

