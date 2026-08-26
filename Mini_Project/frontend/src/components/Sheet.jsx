import { motion, AnimatePresence } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { CloseIcon } from "./Icons";

/** Animated bottom-sheet on mobile / centered modal on desktop, closes via router back-nav. */
export default function Sheet({ title, children, onCloseTo, maxWidth = "max-w-lg" }) {
  const navigate = useNavigate();
  const close = () => (onCloseTo ? navigate(onCloseTo) : navigate(-1));

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-end sm:items-center justify-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={close}
      >
        <motion.div
          className={`glass w-full ${maxWidth} sm:rounded-xl2 rounded-t-xl2 max-h-[90vh] overflow-y-auto shadow-card`}
          initial={{ y: "100%", opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: "100%", opacity: 0 }}
          transition={{ type: "spring", stiffness: 380, damping: 36 }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex items-center justify-between px-6 pt-5 pb-3 sticky top-0 glass z-10">
            <h2 className="text-lg font-display font-bold">{title}</h2>
            <button onClick={close} className="p-2 rounded-full hover:bg-white/10 text-slate-400">
              <CloseIcon className="w-5 h-5" />
            </button>
          </div>
          <div className="px-6 pb-8">{children}</div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
