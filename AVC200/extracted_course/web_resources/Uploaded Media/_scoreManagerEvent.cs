
using UnityEngine;
using TMPro;

public class _scoreManagerEvent : MonoBehaviour
{
    [SerializeField]
    private int score = 0; // Initial score

    [SerializeField]
    private TextMeshProUGUI scoreText; // Reference to the TextMeshPro text field

    public int Score
    {
        get { return score; }
        private set { score = value; }
    }

    // Public function to increment the score and update the TextMeshPro text field
    public void IncrementScore(int amount)
    {
        score += amount;
        UpdateScoreText();
    }

    // Update the TextMeshPro text field with the current score
    private void UpdateScoreText()
    {
        if (scoreText != null)
        {
            scoreText.text = score.ToString(); // Convert int to string
        }
    }
}
