import nextcord

nopings = nextcord.AllowedMentions(replied_user=False)


def split_chunks(input: str, chunks: int = 1990) -> list[str]:
    return [input[n:n + chunks] for n in range(0, len(input), chunks)]
