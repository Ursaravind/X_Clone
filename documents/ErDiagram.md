## ER Diagram
**Link to view**: [https://www.mermaidchart.com/d/5c453b5b-1924-4d56-b93c-b9aa426efbc8](https://www.mermaidchart.com/d/5c453b5b-1924-4d56-b93c-b9aa426efbc8)

### ER Diagram Key Design Points

#### USER Entity
- Differentiates Consumer (Aravind) vs Power User (Elon Musk) with `is_super_user` boolean flag
- `is_verified_badge` field supports Power User verification feature
- `two_factor_enabled` supports high-security authentication requirements
- `handle` and `email` serve as unique identifiers for authentication

#### PROFILE Entity
- Extends USER with additional profile fields (location, website, banner)
- Links directly to USER via `user_id` foreign key
- Supports Consumer profile view/edit functionality

#### SESSION Entity
- Enables high-security authentication tracking for Power Users
- `mfa_passed_at` timestamp records successful multi-factor authentication
- `session_token` and `ip_address` enhance security monitoring

#### FOLLOW Entity
- Implements controlled following mechanism with `is_silent_follow` flag
- When Power User follows someone, `is_silent_follow = TRUE` (no notification)
- Self-referencing relationship between USER entities

#### POST Entity
- Core content entity with rich media support via `body_rich_media_json`
- `max_char_limit` field allows different limits for Consumer vs Power User
- `last_edited_at` supports post editing functionality (Power User only)
- `reply_to_post_id` enables threaded conversations

#### POST_EDIT_HISTORY Entity
- Maintains audit trail of post edits (Power User feature)
- `prior_body_snapshot` preserves previous versions
- `edited_at` timestamp tracks modification history

#### MEDIA Entity
- Supports rich media types (image, video, link-card)
- `quality_tier` field prioritizes HD content for Power Users
- Links posts to multiple media assets

#### INTERACTION Entities (LIKE, COMMENT)
- **LIKE**: Simple user-post interaction tracking
- **COMMENT**: Supports nested replies with `parent_comment_id` self-reference
- Both enable core Consumer engagement features

#### VISIBILITY_BOOST Entity
- Implements algorithmic post promotion for Power User content
- `boost_factor` multiplier enhances post reach and visibility
- `reason` field tracks promotion rationale (Power User priority)

### Key Relationships
- **USER 1:N POST**: One user creates many posts
- **POST 1:N MEDIA**: One post contains multiple media
- **POST 1:N VISIBILITY_BOOST**: Boost applied to specific posts
- **Self-referencing**: FOLLOW, POST replies, COMMENT nesting
- **USER 1:1 PROFILE**: Each user has one profile