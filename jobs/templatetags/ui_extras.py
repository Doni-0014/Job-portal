from django import template

register = template.Library()


@register.filter
def split_skills(skills_csv):
    if not skills_csv:
        return []
    return [s.strip() for s in str(skills_csv).split(',') if s.strip()]


@register.filter
def salary_range(job):
    try:
        min_s = job.min_salary
        max_s = job.max_salary
        if min_s and max_s:
            return f"{min_s:,} - {max_s:,}"
        if min_s:
            return f"{min_s:,}+"
        if max_s:
            return f"Up to {max_s:,}"
    except Exception:
        pass
    return "—"

