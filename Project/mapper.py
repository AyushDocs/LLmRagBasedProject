from Project.ga1 import *
from Project.ga2 import *
from Project.ga3 import *
from Project.ga4 import *
from Project.ga5 import *

TOOL_FUNCTION_MAPPER = {
    # ga1.json mappings
    "check_vs_code_version": None,  # No implementation provided
    "make_http_request_with_uv": make_http_request_with_uv,
    "run_command_with_npx": run_command_with_npx,
    "use_google_sheets": None,  # No implementation provided
    "use_excel": None,  # No implementation provided

    # ga2.json mappings
    "throw_exception": None,  # No implementation provided
    "compress_image": compress_image,
    "deploy_github_pages": deploy_github_pages,
    "authenticate_colab": authenticate_colab,
    "count_light_pixels": count_light_pixels,
    "deploy_vercel": deploy_vercel,
    "create_github_action": create_github_action,
    "push_docker_image": push_docker_image,
    "get_student_data_using_fastapi": get_student_data_using_fastapi,
    "find_most_similar_phrases": highest_ebedding_similarrity_finder_using_cosine_similarity,
    "semantic_search_documents": sort_docs_by_embeddings,
    "map_query_to_function": None,  # No implementation provided
    "bypass_llm_restriction": None,  # No implementation provided

    # ga4.json mappings
    "count_ducks_espn": count_ducks_espn,
    "fetch_imdb_movies": fetch_imdb_movies,
    "fetch_wikipedia_outline": fetch_wikipedia_outline,
    "fetch_weather_san_francisco": fetch_weather_san_francisco,
    "get_cairo_max_lat": get_cairo_max_lat,
    "find_hn_post_signal": find_hn_post_signal,
    "find_newest_github_user_tokyo": find_newest_github_user_tokyo,
    "create_github_action": create_github_action,
    "parse_student_marks": parse_student_marks,
    "pdf_to_markdown": pdf_to_markdown,

    # ga5.json mappings
    "total_margin_theta_sales": total_margin_theta,
    "count_unique_students": count_unique_students,
    "count_successful_malayalam_requests": count_successful_malayalam_requests,
    "top_ip_hindimp3_downloads": top_hindimp3_consumer,
    "count_pizza_sales_jakarta": pizza_sales_jakarta,
    "calculate_total_sales": total_sales,
    "count_key_occurrences": count_key_occurrences,
    "filter_high_quality_posts": find_high_engagement_posts,
    "transcribe_audio_segment": transcribe_video_segment,
    "reconstruct_scrambled_image": reconstruct_image,
}
