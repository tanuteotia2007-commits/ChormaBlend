from flask import Blueprint, request, jsonify, send_file
from middleware.auth_middleware import require_safety_session
from services.document_service import list_documents, save_document, delete_document, get_document_for_download

document_bp = Blueprint("documents", __name__, url_prefix="/api/documents")

@document_bp.route("", methods=["GET"])
@require_safety_session
def get_all_documents():
    """Retrieve all document metadata from the vault."""
    docs = list_documents()
    return jsonify({
        "success": True,
        "data": docs
    }), 200

@document_bp.route("", methods=["POST"])
@require_safety_session
def upload_document():
    """Upload and secure a document file into local vault and SQLite."""
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file part in request"
        }), 400

    file_item = request.files["file"]
    if file_item.filename == "":
        return jsonify({
            "success": False,
            "message": "No selected file"
        }), 400

    try:
        doc_record = save_document(file_item)
        return jsonify({
            "success": True,
            "data": doc_record
        }), 201
    except ValueError as val_err:
        return jsonify({
            "success": False,
            "message": str(val_err)
        }), 400
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": f"Upload failed: {str(exc)}"
        }), 500

@document_bp.route("/<int:document_id>/download", methods=["GET"])
@require_safety_session
def download_document(document_id: int):
    """Securely stream a document file from storage."""
    doc_info = get_document_for_download(document_id)
    if not doc_info:
        return jsonify({
            "success": False,
            "message": "Document not found"
        }), 404

    return send_file(
        str(doc_info["file_path"]),
        as_attachment=True,
        download_name=doc_info["filename"],
        mimetype=doc_info["mime_type"]
    )

@document_bp.route("/<int:document_id>", methods=["DELETE"])
@require_safety_session
def remove_document(document_id: int):
    """Delete a document from local storage and SQLite."""
    deleted = delete_document(document_id)
    if not deleted:
        return jsonify({
            "success": False,
            "message": "Document not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Document deleted"
    }), 200
