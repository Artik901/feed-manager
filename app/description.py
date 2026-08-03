from app.description_manager import (
    get_description_rule
)


def apply_description(
        offer,
        category_ids
):


    rule = None


    # ищем от самой глубокой категории вверх

    for category_id in category_ids:


        rule = get_description_rule(
            category_id
        )


        if rule:

            break



    if not rule:

        return offer
      

    old_description = offer.get(
        "description",
        ""
    )



    before = rule.get(
        "before",
        ""
    )


    after = rule.get(
        "after",
        ""
    )



    parts = []



    if before:

        parts.append(
            before.strip()
        )



    if old_description:

        parts.append(
            old_description.strip()
        )



    if after:

        parts.append(
            after.strip()
        )



    offer["description"] = "\n\n".join(
        parts
    )

    return offer