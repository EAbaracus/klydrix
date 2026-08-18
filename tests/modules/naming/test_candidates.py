import pytest
from launch_engine.modules.naming.candidates import InternalAssessment, NameCandidate, NameCandidateList
from launch_engine.modules.naming.brief import NameTypology
from datetime import datetime, timezone


def test_internal_assessment():
    """Test InternalAssessment model."""
    assessment = InternalAssessment(score=0.8, rationale="Good name")
    assert assessment.score == 0.8
    assert assessment.rationale == "Good name"
    assert assessment.source == "llm_self_assessment"


def test_name_candidate_required_fields():
    """Test NameCandidate with required fields only."""
    candidate = NameCandidate(
        candidate_id="1",
        name="TestName",
        typology=NameTypology.INVENTED,
        rationale="A great invented name"
    )
    assert candidate.candidate_id == "1"
    assert candidate.name == "TestName"
    assert candidate.typology == NameTypology.INVENTED
    assert candidate.rationale == "A great invented name"
    assert candidate.phonetic_notes is None
    assert candidate.tagline_options == []
    assert candidate.brand_story_seed is None
    assert candidate.internal_assessment is None


def test_name_candidate_all_fields():
    """Test NameCandidate with all optional fields."""
    assessment = InternalAssessment(score=0.9, rationale="Excellent")
    candidate = NameCandidate(
        candidate_id="2",
        name="AwesomeName",
        typology=NameTypology.METAPHORICAL,
        rationale="A metaphorical name",
        phonetic_notes="Easy to pronounce",
        tagline_options=["Just do it", "Do it"],
        brand_story_seed="A story about success",
        internal_assessment=assessment
    )
    assert candidate.candidate_id == "2"
    assert candidate.name == "AwesomeName"
    assert candidate.typology == NameTypology.METAPHORICAL
    assert candidate.rationale == "A metaphorical name"
    assert candidate.phonetic_notes == "Easy to pronounce"
    assert candidate.tagline_options == ["Just do it", "Do it"]
    assert candidate.brand_story_seed == "A story about success"
    assert candidate.internal_assessment == assessment


def test_name_candidate_list():
    """Test NameCandidateList model."""
    candidate = NameCandidate(
        candidate_id="1",
        name="TestName",
        typology=NameTypology.INVENTED,
        rationale="A great invented name"
    )
    candidate_list = NameCandidateList(
        brief_ref="brief_123",
        candidates=[candidate],
        llm_model_used="gpt-4",
        llm_provider="openai",
        generated_at=datetime.now(timezone.utc)
    )
    assert candidate_list.brief_ref == "brief_123"
    assert len(candidate_list.candidates) == 1
    assert candidate_list.candidates[0] == candidate
    assert candidate_list.llm_model_used == "gpt-4"
    assert candidate_list.llm_provider == "openai"
    # Check that generated_at is a datetime and timezone-aware
    assert isinstance(candidate_list.generated_at, datetime)
    assert candidate_list.generated_at.tzinfo is not None


def test_candidate_id_required():
    """Test that candidate_id is required (not optional)."""
    # This test is implicit in the model definition: candidate_id is required.
    # We can test that creating without candidate_id raises an error.
    with pytest.raises(Exception):
        NameCandidate(
            # candidate_id missing
            name="TestName",
            typology=NameTypology.INVENTED,
            rationale="A great invented name"
        )